import logging

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tasks.models import Project, Task
from tasks.serializers import ProjectListSerializer, ProjectSerializer, TaskSerializer
from tasks.utilities.responses import forbidden, validation_error

logger = logging.getLogger(__name__)


class ProjectViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        projects = Project.objects.filter(
            Q(owner=request.user) | Q(tasks__assignee=request.user)
        ).distinct().order_by("-created_at")
        serializer = ProjectListSerializer(projects, many=True)
        return Response({"projects": serializer.data})

    def create(self, request):
        serializer = ProjectListSerializer(data=request.data)
        if not serializer.is_valid():
            return validation_error(serializer.errors)

        project = Project.objects.create(owner=request.user, **serializer.validated_data)
        logger.info("Project created: %s by %s", project.id, request.user.email)
        return Response(ProjectListSerializer(project).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        project = get_object_or_404(Project, id=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        project = get_object_or_404(Project, id=pk)
        if project.owner != request.user:
            return forbidden()

        serializer = ProjectListSerializer(project, data=request.data, partial=True)
        if not serializer.is_valid():
            return validation_error(serializer.errors)

        serializer.save()
        logger.info("Project updated: %s", project.id)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        project = get_object_or_404(Project, id=pk)
        if project.owner != request.user:
            return forbidden()

        project_id = project.id
        project.delete()
        logger.info("Project deleted: %s", project_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get", "post"])
    def tasks(self, request, pk=None):
        project = get_object_or_404(Project, id=pk)
        if request.method.lower() == "post":
            serializer = TaskSerializer(data=request.data)
            if not serializer.is_valid():
                return validation_error(serializer.errors)

            task = Task.objects.create(
                project=project,
                **{k: v for k, v in serializer.validated_data.items() if k != "assignee"},
            )
            if "assignee" in serializer.validated_data:
                task.assignee = serializer.validated_data["assignee"]
                task.save()

            logger.info("Task created: %s in project %s", task.id, project.id)
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

        project_tasks = project.tasks.all()
        status_filter = request.query_params.get("status")
        if status_filter:
            project_tasks = project_tasks.filter(status=status_filter)
        assignee_filter = request.query_params.get("assignee")
        if assignee_filter:
            project_tasks = project_tasks.filter(assignee_id=assignee_filter)
        serializer = TaskSerializer(project_tasks.order_by("-created_at"), many=True)
        return Response({"tasks": serializer.data})

    @action(detail=True, methods=["post"], url_path="create_task")
    def create_task(self, request, pk=None):
        # Backward-compatible alias for older clients.
        project = get_object_or_404(Project, id=pk)
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
            return validation_error(serializer.errors)

        task = Task.objects.create(
            project=project,
            **{k: v for k, v in serializer.validated_data.items() if k != "assignee"},
        )
        if "assignee" in serializer.validated_data:
            task.assignee = serializer.validated_data["assignee"]
            task.save()

        logger.info("Task created: %s in project %s", task.id, project.id)
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        project = get_object_or_404(Project, id=pk)
        project_tasks = project.tasks.all()
        status_counts = {
            choice[0]: project_tasks.filter(status=choice[0]).count()
            for choice in Task.STATUS_CHOICES
        }
        assignee_counts = {}
        for task in project_tasks:
            if task.assignee:
                name = task.assignee.name
                assignee_counts[name] = assignee_counts.get(name, 0) + 1

        return Response(
            {
                "status_counts": status_counts,
                "assignee_counts": assignee_counts,
                "total_tasks": project_tasks.count(),
            }
        )


class TaskViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, pk=None):
        task = get_object_or_404(Task, id=pk)
        if task.project.owner != request.user:
            return forbidden()

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if not serializer.is_valid():
            return validation_error(serializer.errors)

        serializer.save()
        logger.info("Task updated: %s", task.id)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        task = get_object_or_404(Task, id=pk)
        if task.project.owner != request.user:
            return forbidden()

        task_id = task.id
        task.delete()
        logger.info("Task deleted: %s", task_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

from typing import Any

from django.core.exceptions import ValidationError
from django.db import models
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django_enum_choices.fields import EnumChoiceField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from src.apps.base.models import TimeStampedMixin, PKIDMixin
from src.other.enums import UnloadServiceType, TimeInterval, TaskStatus


class UnloadScheduler(PKIDMixin, TimeStampedMixin):
    title = models.CharField(max_length=70, verbose_name=_("Название"))
    task = models.OneToOneField(
        PeriodicTask,
        verbose_name=_("Периодическая задача"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    service = EnumChoiceField(
        UnloadServiceType,
        default=UnloadServiceType.fortochki,
        verbose_name=_("Сервис"),
    )
    time_interval = EnumChoiceField(
        TimeInterval,
        default=TimeInterval.five_mins,
        verbose_name=_("Временной интервал"),
    )
    status = EnumChoiceField(
        TaskStatus, default=TaskStatus.active, verbose_name=_("Статус")
    )
    tire_unload = models.BooleanField(default=True)
    rim_unload = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Выгрузка")
        verbose_name_plural = _("Выгрузки")

    @property
    def interval_schedule(self) -> IntervalSchedule:
        if self.time_interval == TimeInterval.one_min:
            return IntervalSchedule.objects.get(every=1, period="minutes")
        if self.time_interval == TimeInterval.five_mins:
            return IntervalSchedule.objects.get(every=5, period="minutes")
        if self.time_interval == TimeInterval.half_hour:
            return IntervalSchedule.objects.get(every=30, period="minutes")
        if self.time_interval == TimeInterval.one_hour:
            return IntervalSchedule.objects.get(every=1, period="hours")
        if self.time_interval == TimeInterval.five_hours:
            return IntervalSchedule.objects.get(every=5, period="hours")
        if self.time_interval == TimeInterval.twelve_hours:
            return IntervalSchedule.objects.get(every=12, period="hours")
        if self.time_interval == TimeInterval.one_day:
            return IntervalSchedule.objects.get(every=1, period="days")
        raise NotImplementedError

    def setup_task(self) -> None:
        if self.service == UnloadServiceType.fortochki:
            task_name = "unload_fortochki_beat"
        else:
            task_name = "unload_starco_beat"
        self.task = PeriodicTask.objects.create(
            name=self.title,
            task=task_name,
            interval=self.interval_schedule,
            start_time=timezone.now(),
        )
        self.save()

    def stop_task(self) -> None:
        self.status = TaskStatus.disabled
        self.save()

    def terminate(self) -> None:
        if self.task is not None:
            self.stop_task()
            ptask = self.task
            self.task = None
            ptask.delete()

    def save(self, *args, **kwargs):
        if not self.pk:
            if (
                self.service == UnloadServiceType.fortochki
                and UnloadScheduler.objects.filter(
                    service=UnloadServiceType.fortochki
                ).exists()
            ):
                raise ValidationError("Unload with this service already created")
            if (
                self.service == UnloadServiceType.starco
                and UnloadScheduler.objects.filter(
                    service=UnloadServiceType.starco
                ).exists()
            ):
                raise ValidationError("Unload with this service already created")
        super(UnloadScheduler, self).save(*args, **kwargs)

    # def delete(self, *args, **kwargs) -> Any:
    #     return super(self.__class__, self).delete(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title}"

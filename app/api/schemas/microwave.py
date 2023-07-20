from datetime import datetime
from datetime import timedelta

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator


class MicrowaveState(BaseModel):
    power: int = Field(600, ge=300, le=1200)
    timer_end_at: datetime = Field(default_factory=datetime.now)

    @field_validator("timer_end_at")
    def validate_timer_end_at(cls, v: datetime):
        if v < datetime.now():
            raise ValueError("Timer end at must be in the future")
        return v

    @property
    def is_microvawe_running(self) -> bool:
        """
        Check if microwave is running
        """
        if self.timer_end_at and self.timer_end_at >= datetime.now():
            return True
        return False

    @property
    def _timer_end_at(self) -> datetime:
        if self.is_microvawe_running:
            return self.timer_end_at
        return datetime.now()

    def inscrease_power(self) -> "MicrowaveState":
        """
        Increase power by 10%
        """
        if self.is_microvawe_running:
            return MicrowaveState(
                power=int(self.power + (self.power * 0.1)),
                timer_end_at=self.timer_end_at,
            )
        return MicrowaveState(
            power=int(self.power + (self.power * 0.1)),
        )

    def decrease_power(self) -> "MicrowaveState":
        """
        Decrease power by 10%
        """
        if self.is_microvawe_running:
            return MicrowaveState(
                power=int(self.power - (self.power * 0.1)),
                timer_end_at=self.timer_end_at,
            )
        return MicrowaveState(
            power=int(self.power - (self.power * 0.1)),
        )

    def increase_timer(self) -> "MicrowaveState":
        """
        Increase counter by 10s
        """
        timer_end_at: datetime = self._timer_end_at
        timer_end_at = timer_end_at + timedelta(seconds=10)

        return MicrowaveState(
            power=self.power,
            timer_end_at=timer_end_at,
        )

    def decrease_timer(self) -> "MicrowaveState":
        """
        Decrease counter by 10s
        """
        timer_end_at: datetime = self.timer_end_at

        seconds_left: float = (timer_end_at - datetime.now()).total_seconds()
        if seconds_left > 0 and seconds_left < 10:
            return MicrowaveState(power=self.power)

        timer_end_at = timer_end_at - timedelta(seconds=10)
        return MicrowaveState(
            power=self.power,
            timer_end_at=timer_end_at,
        )

    def cancel(self) -> "MicrowaveState":
        """
        Cancel heating in microwave
        """
        return MicrowaveState(power=self.power)

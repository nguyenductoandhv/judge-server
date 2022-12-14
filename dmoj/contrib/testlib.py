import re

from dmoj.contrib.default import ContribModule as DefaultContribModule
from dmoj.error import InternalError
from dmoj.result import CheckerResult
from dmoj.utils.helper_files import parse_helper_file_error


class ContribModule(DefaultContribModule):
    AC = 0
    WA = 1
    PE = 2
    IE = 3
    PARTIAL = 7

    name = 'testlib'
    repartial = re.compile(br'^points ([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)', re.M)

    @classmethod
    def get_interactor_args_format_string(cls):
        return '{input_file} {output_file} {answer_file}'

    @classmethod
    @DefaultContribModule.catch_internal_error
    def parse_return_code(
        cls, proc, executor, point_value, time_limit, memory_limit, feedback, extended_feedback, name, stderr
    ):
        if proc.returncode == cls.AC:
            return CheckerResult(True, point_value, feedback=feedback, extended_feedback=extended_feedback)
        elif proc.returncode == cls.PARTIAL:
            match = cls.repartial.search(stderr)
            if not match:
                raise InternalError('Invalid stderr for partial points: %r' % stderr)
            points = float(match.group(1))
            if not 0 <= points <= point_value:
                raise InternalError('Invalid partial points: %f, must be between [%f; %f]' % (points, 0, point_value))
            return CheckerResult(True, points, feedback=feedback, extended_feedback=extended_feedback)
        elif proc.returncode == cls.WA:
            return CheckerResult(False, 0, feedback=feedback, extended_feedback=extended_feedback)
        elif proc.returncode == cls.PE:
            return CheckerResult(
                False, 0, feedback=feedback or 'Presentation Error', extended_feedback=extended_feedback
            )
        elif proc.returncode == cls.IE:
            raise InternalError('%s failed assertion with message %s %s' % (name, feedback, extended_feedback))
        else:
            parse_helper_file_error(proc, executor, name, stderr, time_limit, memory_limit)

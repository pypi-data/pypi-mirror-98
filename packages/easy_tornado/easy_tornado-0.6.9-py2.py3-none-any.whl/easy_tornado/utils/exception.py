# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018/11/19 11:03
from .logging import it_print
from ..compat import C_StandardError
from ..functional import deprecated


class InternalError(C_StandardError):

  def __init__(self, *args, **kwargs):
    super(InternalError, self).__init__(*args, **kwargs)


def raise_print(*args, **kwargs):
  """
  print message and raise InternalError
  :param args: see it_print
  :param kwargs: it_print
  """
  _do_print(*args, **kwargs)
  message = kwargs.pop('message', 'Unknown')
  raise InternalError(message)


def exit_print(*args, **kwargs):
  """
  print message and exit
  :param args: see it_print
  :param kwargs: see it_print
  """
  _do_print(*args, **kwargs)
  errno = kwargs.pop('errno', 0)
  exit(int(errno))


def _do_print(*args, **kwargs):
  if 'device' not in kwargs:
    kwargs['device'] = 2

  print_fn = kwargs.pop('print_fn', it_print)
  print_fn(*args, **kwargs)


@deprecated(new_fn=exit_print)
def error_exit(errno=0, error=None):
  """
  print message and exit
  :param errno: error code
  :param error: error message
  """
  if error is not None:
    it_print(error)
  exit(errno)

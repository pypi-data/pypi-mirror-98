from typing import List, Dict, Any, Optional


def generate_key(
    *, key: str, deeper_args: List[Any], deeper_kwargs: Dict[Any, Any],
    kwargs_list: Optional[List[str]] = None, check_params: bool = False,
    check_args_params: bool = False, check_kwargs_params: bool = False
) -> str:
    kwargs_name = deeper_kwargs
    tail = ''

    if kwargs_list:
        kwargs_name = {kw: deeper_kwargs.get(kw) for kw in kwargs_list}

    if check_params or (check_args_params and check_kwargs_params):
        tail = f'-{deeper_args}-{kwargs_name}'
    elif check_args_params and check_kwargs_params is False:
        tail = f'-{deeper_args}'
    elif check_kwargs_params and check_args_params is False:
        tail = f'-{kwargs_name}'
    return f'{key}{tail}'

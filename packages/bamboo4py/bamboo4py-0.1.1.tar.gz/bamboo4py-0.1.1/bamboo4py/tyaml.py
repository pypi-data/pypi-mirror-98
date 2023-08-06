from typing import Any, Dict, List, Optional, Tuple, Union
import yaml
from pathlib import Path
import re

aByte = 1

aKilobyte = 1000 * aByte
aMegabyte = 1000 * aKilobyte
aGigabyte = 1000 * aMegabyte

aKibibyte = 1024 * aByte
aMebibyte = 1024 * aKibibyte
aGibibyte = 1024 * aMebibyte


def disk_size_str_to_bytes(num: float, unit: str):
    unit = unit.lower()
    if unit == "b":
        return num
    elif unit == "kib":
        return num * aKibibyte
    elif unit == "mib":
        return num * aMebibyte
    elif unit == "gib":
        return num * aGibibyte
    elif unit == "kb":
        return num * aGigabyte
    elif unit == "mb":
        return num * aMegabyte
    elif unit == "gb":
        return num * aGigabyte
    else:
        raise ValueError("unsupported disk size unit")


DISK_SIZE_PATN = re.compile(
    r"^([0-9\.]+)([A-Za-z]+)$")


def read_disk_size(s: str) -> Optional[Tuple[float, str]]:
    s = s.lower()
    m = DISK_SIZE_PATN.match(s)
    if m:
        return float(m[1]), m[2]
    return None


class Document(object):
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self.parent_path = self.file_path.parent
        self.file_content = self.file_path.read_text(encoding="utf-8")

    def expand_path(self, path: str) -> Path:
        if path.startswith("/"):
            return Path(path)
        else:
            return (self.parent_path / path).absolute()

    def parse_yaml(self) -> Dict[str, Any]:
        content = yaml.safe_load(self.file_content)
        assert isinstance(content, Dict)
        return content

    def parse(self, **args):
        yaml_content = self.parse_yaml()
        if "params" in yaml_content:
            yaml_content.pop("params", None)
        result = self.walk_and_replace_values(yaml_content, args)
        return result

    @classmethod
    def check_params(cls, params: Dict[str, str], args: Dict[str, Any]):
        """Check if arguments have correct types in parameters.
        raise `ValueError` if argument type is not fit parameter.
        """
        for k in params:
            if not params[k].endswith("?") and k not in args:
                raise ValueError('required argument "{}" not found'.format(k))
        for k in args:
            if k not in params:
                raise ValueError('arguments "{}" does not fit any parameter'.format(k))
            field_type = params[k]
            if field_type.endswith("?"):
                field_type = field_type[:-1]
            val = args[k]
            if field_type == "string":
                if not isinstance(val, str):
                    raise ValueError('argument "{}": except {}'.format(k, field_type))
            elif field_type == "number":
                if not isinstance(val, (int, float)):
                    raise ValueError('argument "{}": except {}'.format(k, field_type))
            elif field_type == "disk_size":
                if not isinstance(val, str):
                    raise ValueError('argument "{}": except {}'.format(k, field_type))
                t = read_disk_size(val)
                if not t:
                    raise ValueError('argument "{}": except {}'.format(k, field_type))
            else:
                raise ValueError('unregonised type {} for "{}"'.format(field_type, k))

    @classmethod
    def walk_and_replace_values(
        cls, content: Union[List, Dict], args: Dict[str, Any]
    ) -> Union[List, Dict]:
        if isinstance(content, Dict):
            result = {}
            for k in content:
                val = content[k]
                if isinstance(val, str):
                    if val.startswith("$"):
                        var_name = val[1:]
                        if var_name in args:
                            val = args[var_name]
                    elif ("{" in val) and ("}" in val):
                        val = val.format_map(args)
                elif isinstance(val, (List, Dict)):
                    val = cls.walk_and_replace_values(val, args)
                result[k] = val
            return result
        elif isinstance(content, List):
            result_list = []
            for val in content:
                if isinstance(val, str):
                    if val.startswith("$"):
                        var_name = val[1:]
                        if var_name in args:
                            val = args[var_name]
                    elif ("{" in val) and ("}" in val):
                        val = val.format_map(args)
                elif isinstance(val, (List, Dict)):
                    val = cls.walk_and_replace_values(val, args)
                result_list.append(val)
            return result_list

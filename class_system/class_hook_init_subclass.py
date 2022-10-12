# https://stackoverflow.com/questions/45400284/understanding-init-subclass
# metaclass use cases falls into just three categories:
# 1. some initialization code running after class creation  <---
# 2. initialization of descriptors
# 3. keeping the order in which class attributes were defined

from enum import Enum

from base import keep_logger


class RepositoryType(Enum):
    HG = "HG"
    GIT = "GIT"
    SVN = "SVN"
    PERFORCE = "PERFORCE"


class Repository:
    _registry = {t: {} for t in RepositoryType}

    # we should provide default value for each class parameter
    def __init_subclass__(cls, scm_type=None, name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if scm_type is not None:
            cls._registry[scm_type][name] = cls


class MainHgRepository(Repository, scm_type=RepositoryType.HG, name="main"):
    pass


class GenericGitRepository(Repository, scm_type=RepositoryType.GIT):
    pass


class SVNRepository(Repository):
    pass


if __name__ == "__main__":
    keep_logger.info("%s", getattr(Repository, "_registry"))

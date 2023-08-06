# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import List, Optional, Tuple, Union

# Pip
from bullet import SlidePrompt, Bullet, Input, colors

# Local
from .constants import Constants

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ class: Prompt ------------------------------------------------------------- #

class Prompt:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def min_default_python_version(cls) -> float:
        return cls.__prompt((cls.__get_min_default_python_version_prompt(), float))

    @classmethod
    def max_default_python_version(cls) -> float:
        return cls.__prompt((cls.__get_max_default_python_version_prompt(), float))

    @classmethod
    def author(cls, default_username: Optional[str] = None) -> Optional[str]:
        return cls.__prompt((cls.__get_author_prompt(), str)) or default_username

    @classmethod
    def config(
        cls,
        default_author: Optional[str] = None,
        default_git_message: Optional[str] = None
    ) -> Tuple[Optional[str], float, float]:
        author, git_message, min_v, max_v = cls.__prompt([
            (cls.__get_author_prompt(default_author=default_author), str),
            (cls.__get_default_git_message_prompt(default_message=default_git_message), str),
            (cls.__get_min_default_python_version_prompt(), float),
            (cls.__get_max_default_python_version_prompt(), float)
        ])

        return author or default_author, git_message or default_git_message, min_v, max_v

    @classmethod
    def new_package(
        cls,
        passed_package_name: Optional[str] = None,
        default_package_name: Optional[str] = None
    ) -> Tuple[str, str]:
        if passed_package_name:
            package_name = passed_package_name
            description = cls.__prompt([
                (cls.__get_package_description_prompt(), str)
            ])
        else:
            package_name, description = cls.__prompt([
                (cls.__get_package_name_prompt(default_package_name), str),
                (cls.__get_package_description_prompt(), str)
            ])

        return package_name, description


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    # Prompts
    @staticmethod
    def __prompt(
        prompts_with_types: Union[List[Tuple[Union[Bullet, Input], any]], Tuple[Union[Bullet, Input], any]],
        summarize: bool = True
    ) -> Union[List[any], any]:
        if not isinstance(prompts_with_types, list):
            prompts_with_types = [prompts_with_types]

        prompts = [p[0] for p in prompts_with_types]
        types = [p[1] for p in prompts_with_types]

        cli = SlidePrompt(prompts)
        all_res = cli.launch()
        all_res = [res[1] if not isinstance(res[1], tuple) else res[1][0] for res in all_res]
        results = [res if isinstance(res, types[i]) else types[i](res) for i, res in enumerate(all_res)]

        if summarize:
            cli.summarize()

        return results if len(results) > 1 else results[0]


    # Getters

    @staticmethod
    def __get_package_name_prompt(default_package_name: Optional[str] = None) -> Input:
        return Input(
            "Enter package name (will be used on pip when published): ",
            default=default_package_name,
            word_color=colors.foreground["yellow"]
        )

    @staticmethod
    def __get_package_description_prompt(default_package_description: Optional[str] = None) -> Input:
        return Input(
            "Enter package description: ",
            default=default_package_description,
            word_color=colors.foreground["yellow"],
            pattern='.*'
        )

    @staticmethod
    def __get_author_prompt(default_author: Optional[str] = None) -> Input:
        return Input(
            "Author (name) to use for publishing packages and creating licenses: ",
            default=default_author,
            word_color=colors.foreground["yellow"],
            pattern='.*'
        )

    @staticmethod
    def __get_default_git_message_prompt(default_message: Optional[str] = None) -> Input:
        return Input(
            "Default message to use for git commits: ",
            default=default_message,
            word_color=colors.foreground["yellow"],
            pattern='.*'
        )

    @classmethod
    def __get_min_default_python_version_prompt(cls) -> Bullet:
        return cls.__get_bullet_prompt('Minimum default supported python vesion?', choices=Constants.PYTHON_VERSIONS)

    @classmethod
    def __get_max_default_python_version_prompt(cls) -> Bullet:
        return cls.__get_bullet_prompt('Maximum default supported python vesion?', choices=Constants.PYTHON_VERSIONS[::-1])

    @staticmethod
    def __get_bullet_prompt(
        question: str,
        choices: List[str]
    ) -> Bullet:
        return Bullet(
            question,
            choices=choices,
            bullet=">",
            margin=2,
            bullet_color=colors.foreground["black"],
            word_color=colors.foreground["cyan"],
            word_on_switch=colors.foreground["black"],
            background_on_switch=colors.background["cyan"],
            indent=0,
            shift=1,
            pad_right=1,
            return_index=True
        )


# ---------------------------------------------------------------------------------------------------------------------------------------- #
"""
Common podcust tools.
"""


def get_user_input(message: str):
    """
    Present a message to the user and capture user's response.
    Validates that the string is alphanumeric latin characters up to 30 length.
    (Wanting to avoid to have to deal with escapted characters and other weird input.
    Admittedly this should be trusted input but I m in favor of taking the precaution.
    30 alphanumeric characters should allow for complex enough passwords.)

    Args:
      message: Message to pring to the user.

    Returns:
      Reply from the user. Note that this is intended to be a trusted input.
    """

    output = input(message)

    if len(output) > 30:
        raise ValueError("Only type up to 30 characters.")
    elif not output.isalnum():
        raise ValueError("Only type alphanumeric latin characters.")
    else:
        return output

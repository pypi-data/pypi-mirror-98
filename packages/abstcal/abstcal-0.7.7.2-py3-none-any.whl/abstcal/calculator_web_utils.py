# Use the following session to track data
# Reference: https://gist.github.com/tvst/036da038ab3e999a64497f42de966a92
import streamlit as st
from streamlit.report_thread import get_report_ctx


class SessionState(object):
    def __init__(self, **kwargs):
        """A new SessionState object.

        Parameters
        ----------
        **kwargs : any
            Default values for the session state.

        Example
        -------
        >>> session_state = SessionState(user_name='', favorite_color='black')
        >>> session_state.user_name = 'Mary'
        ''
        >>> session_state.favorite_color
        'black'

        """
        for key, val in kwargs.items():
            setattr(self, key, val)


@st.cache(allow_output_mutation=True)
def get_session(id, **kwargs):
    return SessionState(**kwargs)


def get_saved_session(**kwargs):
    """Gets a SessionState object for the current session.

    Creates a new object if necessary.

    Parameters
    ----------
    **kwargs : any
        Default values you want to add to the session state, if we're creating a
        new one.

    Example
    -------
    >>> session_state = get(user_name='', favorite_color='black')
    >>> session_state.user_name
    ''
    >>> session_state.user_name = 'Mary'
    >>> session_state.favorite_color
    'black'

    Since you set user_name above, next time your script runs this will be the
    result:
    >>> session_state = get(user_name='', favorite_color='black')
    >>> session_state.user_name
    'Mary'

    """
    ctx = get_report_ctx()
    id = ctx.session_id
    return get_session(id, **kwargs)


__all__ = ["get_saved_session"]
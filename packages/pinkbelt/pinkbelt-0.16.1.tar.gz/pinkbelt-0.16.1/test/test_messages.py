from mock import patch

from pinkbelt.messages import post_message

@patch("pinkbelt.messages.slack_post_message")
def test_post_message(mock_post_message):
  post_message('test', 'room')
  assert mock_post_message.called, True
  assert mock_post_message.call_args_list, ['test', 'room']

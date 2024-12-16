from typing import Any, Callable

import mesop.labs as mel


@mel.web_component(path="./rating_component.js")
def rating_component(
  *,
  rating: int,
  comment: str,
  on_send_rating: Callable[[mel.WebEvent], Any],
  key: str | None = None,
):
  return mel.insert_web_component(
    name="rating-component",
    key=key,
    events={
      "sendRatingEvent": on_send_rating,
    },
    properties={
      "rating": rating,
      "comment": comment,
    },
  )
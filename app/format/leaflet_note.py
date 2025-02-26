from collections.abc import Iterable

import cython
import numpy as np
from shapely import lib

from app.models.db.note import Note
from app.models.proto.shared_pb2 import RenderNotesData


class LeafletNoteMixin:
    @staticmethod
    def encode_notes(notes: Iterable[Note]) -> RenderNotesData:
        """Format notes into a minimal structure, suitable for map rendering."""
        return RenderNotesData(notes=tuple(_encode_note(note) for note in notes))


@cython.cfunc
def _encode_note(note: Note):
    x, y = lib.get_coordinates(np.asarray(note.point, dtype=np.object_), False, False)[0].tolist()
    body = note.comments[0].body
    if len(body) > 100:
        body = body[:100] + '...'
    return RenderNotesData.Note(
        id=note.id,
        lon=x,
        lat=y,
        text=body,
        open=note.closed_at is None,
    )

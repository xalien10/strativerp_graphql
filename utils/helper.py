def get_obj_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except Exception:
        return None

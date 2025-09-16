def paginate(queryset, skip: int = 0, limit: int = 10):
    """
    Helper para paginar una consulta SQLAlchemy.
    """
    return queryset.offset(skip).limit(limit).all()
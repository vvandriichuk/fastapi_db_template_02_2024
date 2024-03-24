from fastapi import Query
from app.schemas.filters import FilteringParams


def get_filtering_params(
    sort_order: str = Query("ASC", description="Sort order: ASC or DESC"),
    page_size: int = Query(10, ge=1, description="Number of tasks per page"),
    page: int = Query(1, ge=1, description="Page number"),
) -> FilteringParams:
    return FilteringParams(
        sort_order=sort_order,
        page_size=page_size,
        page=page
    )
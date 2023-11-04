from uuid import UUID

from fastapi import APIRouter, Depends

from app.api import deps
from app.payment.schemas.spot_bill import SpotBillCreate, SpotBillView
from app.payment.services.spot_bill import SpotBillService

router = APIRouter()
validate_token = deps.token_auth()


@router.post(
    "/",
    response_model=SpotBillView,
    dependencies=[Depends(deps.hass_access)],
)
def create_spot_bill(
    spot_bill: SpotBillCreate,
    id_user: UUID = Depends(deps.get_id_user_by_auth_token),
    service: SpotBillService = Depends(deps.get_spot_bill_service),
):
    return service.create(id_user=id_user, create=spot_bill)


# @router.get("/", response_model=List[SpotView], dependencies=[Security(validate_token)])
# def get_all(
#     service: SpotService = Depends(deps.get_spot_service),
#     filters: SpotSearchParams = Depends(SpotGetParams.params()),
# ):
#     return service.get_all(params=filters)

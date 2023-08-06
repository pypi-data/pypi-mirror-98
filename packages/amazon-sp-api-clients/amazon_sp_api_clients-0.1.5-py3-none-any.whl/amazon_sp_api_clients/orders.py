from .base import BaseClient as __BaseClient
from typing import List as _List


class GetOrdersResponse:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "payload" in data:
            self.payload: OrdersList = OrdersList(data["payload"])
        else:
            self.payload: OrdersList = None
        if "errors" in data:
            self.errors: ErrorList = ErrorList(data["errors"])
        else:
            self.errors: ErrorList = None


class GetOrderResponse:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "payload" in data:
            self.payload: Order = Order(data["payload"])
        else:
            self.payload: Order = None
        if "errors" in data:
            self.errors: ErrorList = ErrorList(data["errors"])
        else:
            self.errors: ErrorList = None


class GetOrderBuyerInfoResponse:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "payload" in data:
            self.payload: OrderBuyerInfo = OrderBuyerInfo(data["payload"])
        else:
            self.payload: OrderBuyerInfo = None
        if "errors" in data:
            self.errors: ErrorList = ErrorList(data["errors"])
        else:
            self.errors: ErrorList = None


class GetOrderAddressResponse:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "payload" in data:
            self.payload: OrderAddress = OrderAddress(data["payload"])
        else:
            self.payload: OrderAddress = None
        if "errors" in data:
            self.errors: ErrorList = ErrorList(data["errors"])
        else:
            self.errors: ErrorList = None


class GetOrderItemsResponse:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "payload" in data:
            self.payload: OrderItemsList = OrderItemsList(data["payload"])
        else:
            self.payload: OrderItemsList = None
        if "errors" in data:
            self.errors: ErrorList = ErrorList(data["errors"])
        else:
            self.errors: ErrorList = None


class GetOrderItemsBuyerInfoResponse:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "payload" in data:
            self.payload: OrderItemsBuyerInfoList = OrderItemsBuyerInfoList(data["payload"])
        else:
            self.payload: OrderItemsBuyerInfoList = None
        if "errors" in data:
            self.errors: ErrorList = ErrorList(data["errors"])
        else:
            self.errors: ErrorList = None


class OrdersList:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "Orders" in data:
            self.Orders: OrderList = OrderList(data["Orders"])
        else:
            self.Orders: OrderList = None
        if "NextToken" in data:
            self.NextToken: str = str(data["NextToken"])
        else:
            self.NextToken: str = None
        if "LastUpdatedBefore" in data:
            self.LastUpdatedBefore: str = str(data["LastUpdatedBefore"])
        else:
            self.LastUpdatedBefore: str = None
        if "CreatedBefore" in data:
            self.CreatedBefore: str = str(data["CreatedBefore"])
        else:
            self.CreatedBefore: str = None


class Order:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "AmazonOrderId" in data:
            self.AmazonOrderId: str = str(data["AmazonOrderId"])
        else:
            self.AmazonOrderId: str = None
        if "SellerOrderId" in data:
            self.SellerOrderId: str = str(data["SellerOrderId"])
        else:
            self.SellerOrderId: str = None
        if "PurchaseDate" in data:
            self.PurchaseDate: str = str(data["PurchaseDate"])
        else:
            self.PurchaseDate: str = None
        if "LastUpdateDate" in data:
            self.LastUpdateDate: str = str(data["LastUpdateDate"])
        else:
            self.LastUpdateDate: str = None
        if "OrderStatus" in data:
            self.OrderStatus: str = str(data["OrderStatus"])
        else:
            self.OrderStatus: str = None
        if "FulfillmentChannel" in data:
            self.FulfillmentChannel: str = str(data["FulfillmentChannel"])
        else:
            self.FulfillmentChannel: str = None
        if "SalesChannel" in data:
            self.SalesChannel: str = str(data["SalesChannel"])
        else:
            self.SalesChannel: str = None
        if "OrderChannel" in data:
            self.OrderChannel: str = str(data["OrderChannel"])
        else:
            self.OrderChannel: str = None
        if "ShipServiceLevel" in data:
            self.ShipServiceLevel: str = str(data["ShipServiceLevel"])
        else:
            self.ShipServiceLevel: str = None
        if "OrderTotal" in data:
            self.OrderTotal: Money = Money(data["OrderTotal"])
        else:
            self.OrderTotal: Money = None
        if "NumberOfItemsShipped" in data:
            self.NumberOfItemsShipped: int = int(data["NumberOfItemsShipped"])
        else:
            self.NumberOfItemsShipped: int = None
        if "NumberOfItemsUnshipped" in data:
            self.NumberOfItemsUnshipped: int = int(data["NumberOfItemsUnshipped"])
        else:
            self.NumberOfItemsUnshipped: int = None
        if "PaymentExecutionDetail" in data:
            self.PaymentExecutionDetail: PaymentExecutionDetailItemList = PaymentExecutionDetailItemList(
                data["PaymentExecutionDetail"]
            )
        else:
            self.PaymentExecutionDetail: PaymentExecutionDetailItemList = None
        if "PaymentMethod" in data:
            self.PaymentMethod: str = str(data["PaymentMethod"])
        else:
            self.PaymentMethod: str = None
        if "PaymentMethodDetails" in data:
            self.PaymentMethodDetails: PaymentMethodDetailItemList = PaymentMethodDetailItemList(
                data["PaymentMethodDetails"]
            )
        else:
            self.PaymentMethodDetails: PaymentMethodDetailItemList = None
        if "MarketplaceId" in data:
            self.MarketplaceId: str = str(data["MarketplaceId"])
        else:
            self.MarketplaceId: str = None
        if "ShipmentServiceLevelCategory" in data:
            self.ShipmentServiceLevelCategory: str = str(data["ShipmentServiceLevelCategory"])
        else:
            self.ShipmentServiceLevelCategory: str = None
        if "EasyShipShipmentStatus" in data:
            self.EasyShipShipmentStatus: str = str(data["EasyShipShipmentStatus"])
        else:
            self.EasyShipShipmentStatus: str = None
        if "CbaDisplayableShippingLabel" in data:
            self.CbaDisplayableShippingLabel: str = str(data["CbaDisplayableShippingLabel"])
        else:
            self.CbaDisplayableShippingLabel: str = None
        if "OrderType" in data:
            self.OrderType: str = str(data["OrderType"])
        else:
            self.OrderType: str = None
        if "EarliestShipDate" in data:
            self.EarliestShipDate: str = str(data["EarliestShipDate"])
        else:
            self.EarliestShipDate: str = None
        if "LatestShipDate" in data:
            self.LatestShipDate: str = str(data["LatestShipDate"])
        else:
            self.LatestShipDate: str = None
        if "EarliestDeliveryDate" in data:
            self.EarliestDeliveryDate: str = str(data["EarliestDeliveryDate"])
        else:
            self.EarliestDeliveryDate: str = None
        if "LatestDeliveryDate" in data:
            self.LatestDeliveryDate: str = str(data["LatestDeliveryDate"])
        else:
            self.LatestDeliveryDate: str = None
        if "IsBusinessOrder" in data:
            self.IsBusinessOrder: bool = bool(data["IsBusinessOrder"])
        else:
            self.IsBusinessOrder: bool = None
        if "IsPrime" in data:
            self.IsPrime: bool = bool(data["IsPrime"])
        else:
            self.IsPrime: bool = None
        if "IsPremiumOrder" in data:
            self.IsPremiumOrder: bool = bool(data["IsPremiumOrder"])
        else:
            self.IsPremiumOrder: bool = None
        if "IsGlobalExpressEnabled" in data:
            self.IsGlobalExpressEnabled: bool = bool(data["IsGlobalExpressEnabled"])
        else:
            self.IsGlobalExpressEnabled: bool = None
        if "ReplacedOrderId" in data:
            self.ReplacedOrderId: str = str(data["ReplacedOrderId"])
        else:
            self.ReplacedOrderId: str = None
        if "IsReplacementOrder" in data:
            self.IsReplacementOrder: bool = bool(data["IsReplacementOrder"])
        else:
            self.IsReplacementOrder: bool = None
        if "PromiseResponseDueDate" in data:
            self.PromiseResponseDueDate: str = str(data["PromiseResponseDueDate"])
        else:
            self.PromiseResponseDueDate: str = None
        if "IsEstimatedShipDateSet" in data:
            self.IsEstimatedShipDateSet: bool = bool(data["IsEstimatedShipDateSet"])
        else:
            self.IsEstimatedShipDateSet: bool = None
        if "IsSoldByAB" in data:
            self.IsSoldByAB: bool = bool(data["IsSoldByAB"])
        else:
            self.IsSoldByAB: bool = None
        if "AssignedShipFromLocationAddress" in data:
            self.AssignedShipFromLocationAddress: Address = Address(data["AssignedShipFromLocationAddress"])
        else:
            self.AssignedShipFromLocationAddress: Address = None
        if "FulfillmentInstruction" in data:
            self.FulfillmentInstruction: FulfillmentInstruction = FulfillmentInstruction(data["FulfillmentInstruction"])
        else:
            self.FulfillmentInstruction: FulfillmentInstruction = None


class OrderBuyerInfo:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "AmazonOrderId" in data:
            self.AmazonOrderId: str = str(data["AmazonOrderId"])
        else:
            self.AmazonOrderId: str = None
        if "BuyerEmail" in data:
            self.BuyerEmail: str = str(data["BuyerEmail"])
        else:
            self.BuyerEmail: str = None
        if "BuyerName" in data:
            self.BuyerName: str = str(data["BuyerName"])
        else:
            self.BuyerName: str = None
        if "BuyerCounty" in data:
            self.BuyerCounty: str = str(data["BuyerCounty"])
        else:
            self.BuyerCounty: str = None
        if "BuyerTaxInfo" in data:
            self.BuyerTaxInfo: BuyerTaxInfo = BuyerTaxInfo(data["BuyerTaxInfo"])
        else:
            self.BuyerTaxInfo: BuyerTaxInfo = None
        if "PurchaseOrderNumber" in data:
            self.PurchaseOrderNumber: str = str(data["PurchaseOrderNumber"])
        else:
            self.PurchaseOrderNumber: str = None


class OrderAddress:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "AmazonOrderId" in data:
            self.AmazonOrderId: str = str(data["AmazonOrderId"])
        else:
            self.AmazonOrderId: str = None
        if "ShippingAddress" in data:
            self.ShippingAddress: Address = Address(data["ShippingAddress"])
        else:
            self.ShippingAddress: Address = None


class Address:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "Name" in data:
            self.Name: str = str(data["Name"])
        else:
            self.Name: str = None
        if "AddressLine1" in data:
            self.AddressLine1: str = str(data["AddressLine1"])
        else:
            self.AddressLine1: str = None
        if "AddressLine2" in data:
            self.AddressLine2: str = str(data["AddressLine2"])
        else:
            self.AddressLine2: str = None
        if "AddressLine3" in data:
            self.AddressLine3: str = str(data["AddressLine3"])
        else:
            self.AddressLine3: str = None
        if "City" in data:
            self.City: str = str(data["City"])
        else:
            self.City: str = None
        if "County" in data:
            self.County: str = str(data["County"])
        else:
            self.County: str = None
        if "District" in data:
            self.District: str = str(data["District"])
        else:
            self.District: str = None
        if "StateOrRegion" in data:
            self.StateOrRegion: str = str(data["StateOrRegion"])
        else:
            self.StateOrRegion: str = None
        if "Municipality" in data:
            self.Municipality: str = str(data["Municipality"])
        else:
            self.Municipality: str = None
        if "PostalCode" in data:
            self.PostalCode: str = str(data["PostalCode"])
        else:
            self.PostalCode: str = None
        if "CountryCode" in data:
            self.CountryCode: str = str(data["CountryCode"])
        else:
            self.CountryCode: str = None
        if "Phone" in data:
            self.Phone: str = str(data["Phone"])
        else:
            self.Phone: str = None
        if "AddressType" in data:
            self.AddressType: str = str(data["AddressType"])
        else:
            self.AddressType: str = None


class Money:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "CurrencyCode" in data:
            self.CurrencyCode: str = str(data["CurrencyCode"])
        else:
            self.CurrencyCode: str = None
        if "Amount" in data:
            self.Amount: str = str(data["Amount"])
        else:
            self.Amount: str = None


class PaymentExecutionDetailItem:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "Payment" in data:
            self.Payment: Money = Money(data["Payment"])
        else:
            self.Payment: Money = None
        if "PaymentMethod" in data:
            self.PaymentMethod: str = str(data["PaymentMethod"])
        else:
            self.PaymentMethod: str = None


class BuyerTaxInfo:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "CompanyLegalName" in data:
            self.CompanyLegalName: str = str(data["CompanyLegalName"])
        else:
            self.CompanyLegalName: str = None
        if "TaxingRegion" in data:
            self.TaxingRegion: str = str(data["TaxingRegion"])
        else:
            self.TaxingRegion: str = None
        if "TaxClassifications" in data:
            self.TaxClassifications: _List[TaxClassification] = [
                TaxClassification(datum) for datum in data["TaxClassifications"]
            ]
        else:
            self.TaxClassifications: _List[TaxClassification] = []


class TaxClassification:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "Name" in data:
            self.Name: str = str(data["Name"])
        else:
            self.Name: str = None
        if "Value" in data:
            self.Value: str = str(data["Value"])
        else:
            self.Value: str = None


class OrderItemsList:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "OrderItems" in data:
            self.OrderItems: OrderItemList = OrderItemList(data["OrderItems"])
        else:
            self.OrderItems: OrderItemList = None
        if "NextToken" in data:
            self.NextToken: str = str(data["NextToken"])
        else:
            self.NextToken: str = None
        if "AmazonOrderId" in data:
            self.AmazonOrderId: str = str(data["AmazonOrderId"])
        else:
            self.AmazonOrderId: str = None


class OrderItem:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "ASIN" in data:
            self.ASIN: str = str(data["ASIN"])
        else:
            self.ASIN: str = None
        if "SellerSKU" in data:
            self.SellerSKU: str = str(data["SellerSKU"])
        else:
            self.SellerSKU: str = None
        if "OrderItemId" in data:
            self.OrderItemId: str = str(data["OrderItemId"])
        else:
            self.OrderItemId: str = None
        if "Title" in data:
            self.Title: str = str(data["Title"])
        else:
            self.Title: str = None
        if "QuantityOrdered" in data:
            self.QuantityOrdered: int = int(data["QuantityOrdered"])
        else:
            self.QuantityOrdered: int = None
        if "QuantityShipped" in data:
            self.QuantityShipped: int = int(data["QuantityShipped"])
        else:
            self.QuantityShipped: int = None
        if "ProductInfo" in data:
            self.ProductInfo: ProductInfoDetail = ProductInfoDetail(data["ProductInfo"])
        else:
            self.ProductInfo: ProductInfoDetail = None
        if "PointsGranted" in data:
            self.PointsGranted: PointsGrantedDetail = PointsGrantedDetail(data["PointsGranted"])
        else:
            self.PointsGranted: PointsGrantedDetail = None
        if "ItemPrice" in data:
            self.ItemPrice: Money = Money(data["ItemPrice"])
        else:
            self.ItemPrice: Money = None
        if "ShippingPrice" in data:
            self.ShippingPrice: Money = Money(data["ShippingPrice"])
        else:
            self.ShippingPrice: Money = None
        if "ItemTax" in data:
            self.ItemTax: Money = Money(data["ItemTax"])
        else:
            self.ItemTax: Money = None
        if "ShippingTax" in data:
            self.ShippingTax: Money = Money(data["ShippingTax"])
        else:
            self.ShippingTax: Money = None
        if "ShippingDiscount" in data:
            self.ShippingDiscount: Money = Money(data["ShippingDiscount"])
        else:
            self.ShippingDiscount: Money = None
        if "ShippingDiscountTax" in data:
            self.ShippingDiscountTax: Money = Money(data["ShippingDiscountTax"])
        else:
            self.ShippingDiscountTax: Money = None
        if "PromotionDiscount" in data:
            self.PromotionDiscount: Money = Money(data["PromotionDiscount"])
        else:
            self.PromotionDiscount: Money = None
        if "PromotionDiscountTax" in data:
            self.PromotionDiscountTax: Money = Money(data["PromotionDiscountTax"])
        else:
            self.PromotionDiscountTax: Money = None
        if "PromotionIds" in data:
            self.PromotionIds: PromotionIdList = PromotionIdList(data["PromotionIds"])
        else:
            self.PromotionIds: PromotionIdList = None
        if "CODFee" in data:
            self.CODFee: Money = Money(data["CODFee"])
        else:
            self.CODFee: Money = None
        if "CODFeeDiscount" in data:
            self.CODFeeDiscount: Money = Money(data["CODFeeDiscount"])
        else:
            self.CODFeeDiscount: Money = None
        if "IsGift" in data:
            self.IsGift: bool = bool(data["IsGift"])
        else:
            self.IsGift: bool = None
        if "ConditionNote" in data:
            self.ConditionNote: str = str(data["ConditionNote"])
        else:
            self.ConditionNote: str = None
        if "ConditionId" in data:
            self.ConditionId: str = str(data["ConditionId"])
        else:
            self.ConditionId: str = None
        if "ConditionSubtypeId" in data:
            self.ConditionSubtypeId: str = str(data["ConditionSubtypeId"])
        else:
            self.ConditionSubtypeId: str = None
        if "ScheduledDeliveryStartDate" in data:
            self.ScheduledDeliveryStartDate: str = str(data["ScheduledDeliveryStartDate"])
        else:
            self.ScheduledDeliveryStartDate: str = None
        if "ScheduledDeliveryEndDate" in data:
            self.ScheduledDeliveryEndDate: str = str(data["ScheduledDeliveryEndDate"])
        else:
            self.ScheduledDeliveryEndDate: str = None
        if "PriceDesignation" in data:
            self.PriceDesignation: str = str(data["PriceDesignation"])
        else:
            self.PriceDesignation: str = None
        if "TaxCollection" in data:
            self.TaxCollection: TaxCollection = TaxCollection(data["TaxCollection"])
        else:
            self.TaxCollection: TaxCollection = None
        if "SerialNumberRequired" in data:
            self.SerialNumberRequired: bool = bool(data["SerialNumberRequired"])
        else:
            self.SerialNumberRequired: bool = None
        if "IsTransparency" in data:
            self.IsTransparency: bool = bool(data["IsTransparency"])
        else:
            self.IsTransparency: bool = None
        if "IossNumber" in data:
            self.IossNumber: str = str(data["IossNumber"])
        else:
            self.IossNumber: str = None
        if "DeemedResellerCategory" in data:
            self.DeemedResellerCategory: str = str(data["DeemedResellerCategory"])
        else:
            self.DeemedResellerCategory: str = None


class OrderItemsBuyerInfoList:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "OrderItems" in data:
            self.OrderItems: OrderItemBuyerInfoList = OrderItemBuyerInfoList(data["OrderItems"])
        else:
            self.OrderItems: OrderItemBuyerInfoList = None
        if "NextToken" in data:
            self.NextToken: str = str(data["NextToken"])
        else:
            self.NextToken: str = None
        if "AmazonOrderId" in data:
            self.AmazonOrderId: str = str(data["AmazonOrderId"])
        else:
            self.AmazonOrderId: str = None


class OrderItemBuyerInfo:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "OrderItemId" in data:
            self.OrderItemId: str = str(data["OrderItemId"])
        else:
            self.OrderItemId: str = None
        if "BuyerCustomizedInfo" in data:
            self.BuyerCustomizedInfo: BuyerCustomizedInfoDetail = BuyerCustomizedInfoDetail(data["BuyerCustomizedInfo"])
        else:
            self.BuyerCustomizedInfo: BuyerCustomizedInfoDetail = None
        if "GiftWrapPrice" in data:
            self.GiftWrapPrice: Money = Money(data["GiftWrapPrice"])
        else:
            self.GiftWrapPrice: Money = None
        if "GiftWrapTax" in data:
            self.GiftWrapTax: Money = Money(data["GiftWrapTax"])
        else:
            self.GiftWrapTax: Money = None
        if "GiftMessageText" in data:
            self.GiftMessageText: str = str(data["GiftMessageText"])
        else:
            self.GiftMessageText: str = None
        if "GiftWrapLevel" in data:
            self.GiftWrapLevel: str = str(data["GiftWrapLevel"])
        else:
            self.GiftWrapLevel: str = None


class PointsGrantedDetail:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "PointsNumber" in data:
            self.PointsNumber: int = int(data["PointsNumber"])
        else:
            self.PointsNumber: int = None
        if "PointsMonetaryValue" in data:
            self.PointsMonetaryValue: Money = Money(data["PointsMonetaryValue"])
        else:
            self.PointsMonetaryValue: Money = None


class ProductInfoDetail:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "NumberOfItems" in data:
            self.NumberOfItems: int = int(data["NumberOfItems"])
        else:
            self.NumberOfItems: int = None


class BuyerCustomizedInfoDetail:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "CustomizedURL" in data:
            self.CustomizedURL: str = str(data["CustomizedURL"])
        else:
            self.CustomizedURL: str = None


class TaxCollection:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "Model" in data:
            self.Model: str = str(data["Model"])
        else:
            self.Model: str = None
        if "ResponsibleParty" in data:
            self.ResponsibleParty: str = str(data["ResponsibleParty"])
        else:
            self.ResponsibleParty: str = None


class FulfillmentInstruction:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "FulfillmentSupplySourceId" in data:
            self.FulfillmentSupplySourceId: str = str(data["FulfillmentSupplySourceId"])
        else:
            self.FulfillmentSupplySourceId: str = None


class Error:
    def __init__(self, data):
        super().__init__()
        self.data = data
        if "code" in data:
            self.code: str = str(data["code"])
        else:
            self.code: str = None
        if "message" in data:
            self.message: str = str(data["message"])
        else:
            self.message: str = None
        if "details" in data:
            self.details: str = str(data["details"])
        else:
            self.details: str = None


class OrderList(list, _List["Order"]):
    def __init__(self, data):
        super().__init__([Order(datum) for datum in data])
        self.data = data


class PaymentMethodDetailItemList(list, _List["str"]):
    def __init__(self, data):
        super().__init__([str(datum) for datum in data])
        self.data = data


class PaymentExecutionDetailItemList(list, _List["PaymentExecutionDetailItem"]):
    def __init__(self, data):
        super().__init__([PaymentExecutionDetailItem(datum) for datum in data])
        self.data = data


class OrderItemList(list, _List["OrderItem"]):
    def __init__(self, data):
        super().__init__([OrderItem(datum) for datum in data])
        self.data = data


class OrderItemBuyerInfoList(list, _List["OrderItemBuyerInfo"]):
    def __init__(self, data):
        super().__init__([OrderItemBuyerInfo(datum) for datum in data])
        self.data = data


class PromotionIdList(list, _List["str"]):
    def __init__(self, data):
        super().__init__([str(datum) for datum in data])
        self.data = data


class ErrorList(list, _List["Error"]):
    def __init__(self, data):
        super().__init__([Error(datum) for datum in data])
        self.data = data


class OrdersClient(__BaseClient):
    def getOrders(
        self,
        MarketplaceIds: _List[str],
        CreatedAfter: str = None,
        CreatedBefore: str = None,
        LastUpdatedAfter: str = None,
        LastUpdatedBefore: str = None,
        OrderStatuses: _List[str] = None,
        FulfillmentChannels: _List[str] = None,
        PaymentMethods: _List[str] = None,
        BuyerEmail: str = None,
        SellerOrderId: str = None,
        MaxResultsPerPage: int = None,
        EasyShipShipmentStatuses: _List[str] = None,
        NextToken: str = None,
        AmazonOrderIds: _List[str] = None,
    ):
        url = "/orders/v0/orders".format()
        data = {}
        if CreatedAfter is not None:
            data["CreatedAfter"] = (CreatedAfter,)
        if CreatedBefore is not None:
            data["CreatedBefore"] = (CreatedBefore,)
        if LastUpdatedAfter is not None:
            data["LastUpdatedAfter"] = (LastUpdatedAfter,)
        if LastUpdatedBefore is not None:
            data["LastUpdatedBefore"] = (LastUpdatedBefore,)
        if OrderStatuses is not None:
            data["OrderStatuses"] = ",".join(map(str, OrderStatuses))
        if MarketplaceIds is not None:
            data["MarketplaceIds"] = ",".join(map(str, MarketplaceIds))
        if FulfillmentChannels is not None:
            data["FulfillmentChannels"] = ",".join(map(str, FulfillmentChannels))
        if PaymentMethods is not None:
            data["PaymentMethods"] = ",".join(map(str, PaymentMethods))
        if BuyerEmail is not None:
            data["BuyerEmail"] = (BuyerEmail,)
        if SellerOrderId is not None:
            data["SellerOrderId"] = (SellerOrderId,)
        if MaxResultsPerPage is not None:
            data["MaxResultsPerPage"] = (MaxResultsPerPage,)
        if EasyShipShipmentStatuses is not None:
            data["EasyShipShipmentStatuses"] = ",".join(map(str, EasyShipShipmentStatuses))
        if NextToken is not None:
            data["NextToken"] = (NextToken,)
        if AmazonOrderIds is not None:
            data["AmazonOrderIds"] = ",".join(map(str, AmazonOrderIds))
        response = self.request(url, method="GET", params=data)
        return {
            200: GetOrdersResponse,
            400: GetOrdersResponse,
            403: GetOrdersResponse,
            404: GetOrdersResponse,
            429: GetOrdersResponse,
            500: GetOrdersResponse,
            503: GetOrdersResponse,
        }[response.status_code](response.json())

    def getOrder(
        self,
        orderId: str,
    ):
        url = "/orders/v0/orders/{orderId}".format(
            orderId=orderId,
        )
        data = {}
        response = self.request(url, method="GET", params=data)
        return {
            200: GetOrderResponse,
            400: GetOrderResponse,
            403: GetOrderResponse,
            404: GetOrderResponse,
            429: GetOrderResponse,
            500: GetOrderResponse,
            503: GetOrderResponse,
        }[response.status_code](response.json())

    def getOrderBuyerInfo(
        self,
        orderId: str,
    ):
        url = "/orders/v0/orders/{orderId}/buyerInfo".format(
            orderId=orderId,
        )
        data = {}
        response = self.request(url, method="GET", params=data)
        return {
            200: GetOrderBuyerInfoResponse,
            400: GetOrderBuyerInfoResponse,
            403: GetOrderBuyerInfoResponse,
            404: GetOrderBuyerInfoResponse,
            429: GetOrderBuyerInfoResponse,
            500: GetOrderBuyerInfoResponse,
            503: GetOrderBuyerInfoResponse,
        }[response.status_code](response.json())

    def getOrderAddress(
        self,
        orderId: str,
    ):
        url = "/orders/v0/orders/{orderId}/address".format(
            orderId=orderId,
        )
        data = {}
        response = self.request(url, method="GET", params=data)
        return {
            200: GetOrderAddressResponse,
            400: GetOrderAddressResponse,
            403: GetOrderAddressResponse,
            404: GetOrderAddressResponse,
            429: GetOrderAddressResponse,
            500: GetOrderAddressResponse,
            503: GetOrderAddressResponse,
        }[response.status_code](response.json())

    def getOrderItems(
        self,
        orderId: str,
        NextToken: str = None,
    ):
        url = "/orders/v0/orders/{orderId}/orderItems".format(
            orderId=orderId,
        )
        data = {}
        if NextToken is not None:
            data["NextToken"] = (NextToken,)
        response = self.request(url, method="GET", params=data)
        return {
            200: GetOrderItemsResponse,
            400: GetOrderItemsResponse,
            403: GetOrderItemsResponse,
            404: GetOrderItemsResponse,
            429: GetOrderItemsResponse,
            500: GetOrderItemsResponse,
            503: GetOrderItemsResponse,
        }[response.status_code](response.json())

    def getOrderItemsBuyerInfo(
        self,
        orderId: str,
        NextToken: str = None,
    ):
        url = "/orders/v0/orders/{orderId}/orderItems/buyerInfo".format(
            orderId=orderId,
        )
        data = {}
        if NextToken is not None:
            data["NextToken"] = (NextToken,)
        response = self.request(url, method="GET", params=data)
        return {
            200: GetOrderItemsBuyerInfoResponse,
            400: GetOrderItemsBuyerInfoResponse,
            403: GetOrderItemsBuyerInfoResponse,
            404: GetOrderItemsBuyerInfoResponse,
            429: GetOrderItemsBuyerInfoResponse,
            500: GetOrderItemsBuyerInfoResponse,
            503: GetOrderItemsBuyerInfoResponse,
        }[response.status_code](response.json())

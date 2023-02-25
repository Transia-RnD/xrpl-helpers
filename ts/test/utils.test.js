const {
  fromCurrencyToHex,
  fromHexToCurrency,
  buildNFTokenID,
  buildNFTokenOfferID,
  buildXrplID,
  parseXrplID,
} = require("../dist/npm/src");

const testMap = [
  {
    currency: "USDC",
    hex: "5553444300000000000000000000000000000000",
  },
  {
    currency: "CORE",
    hex: "434F524500000000000000000000000000000000",
  },
  {
    currency: "SOLO",
    hex: "534F4C4F00000000000000000000000000000000",
  },
  {
    currency: "IUSD",
    hex: "4955534400000000000000000000000000000000",
  },
];

describe("test convert fromCurrencyToHex & fromHexToCurrency", function () {
  it("test map", function () {
    testMap.forEach((testMap) => {
      const fromResponse = fromCurrencyToHex(testMap.currency);
      expect(fromResponse).toEqual(testMap.hex);
      const toResponse = fromHexToCurrency(testMap.hex);
      expect(toResponse == testMap.currency);
    });
  });
});

describe("test build nftokenID", function () {
  it("buildNFTokenID", function () {
    const flags = 11;
    const fee = 1337;
    const sequence = 12;
    const taxon = 1337;
    const result = buildNFTokenID(
      flags,
      fee,
      "rJoxBSzpXhPtAuqFmqxQtGKjA13jUJWthE",
      sequence,
      taxon
    );
    expect(result).toEqual(
      "000B0539C35B55AA096BA6D87A6E6C965A6534150DC56E5E12C5D09E0000000C"
    );
  });
});

describe("test build offerID", function () {
  it("buildOfferID", function () {
    const account = "rJpMn8yEHeWSQ6w581dJsk8Z2jhCUEWbwD";
    const accountSeq = 538710;
    const response = buildNFTokenOfferID(account, accountSeq);
    expect(response).toEqual(
      "A520BF32C8CB877703D3E6E2FE71BC2FF0347A3C6A6C92092956D7E8D39ADD40"
    );
  });
});

describe("test build xrplID", function () {
  it("buildXrplID", function () {
    const result = buildXrplID(
      1, // 1 = LedgerEntryType, 2 = TransactionType, 3 = Account
      111, // Offer LE
      "A520BF32C8CB877703D3E6E2FE71BC2FF0347A3C6A6C92092956D7E8D39ADD40",
      51235
    );
    expect(result).toEqual(
      "0001006FA520BF32C8CB877703D3E6E2FE71BC2FF0347A3C6A6C92092956D7E8D39ADD400000C823"
    );
  });
});

describe("test parse xrplID", function () {
  it("parseXrplID", function () {
    const result = parseXrplID(
      "0001006FA520BF32C8CB877703D3E6E2FE71BC2FF0347A3C6A6C92092956D7E8D39ADD400000C823"
    );
    expect(result).toEqual({
      hash: "A520BF32C8CB877703D3E6E2FE71BC2FF0347A3C6A6C92092956D7E8D39ADD40",
      network: 51235,
      type: 1,
      subtype: 111,
      xrplID:
        "0001006FA520BF32C8CB877703D3E6E2FE71BC2FF0347A3C6A6C92092956D7E8D39ADD400000C823",
    });
  });
});

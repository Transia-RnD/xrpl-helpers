const { 
  fromCurrencyToHex,
  fromHexToCurrency,
  buildNFTokenID,
  buildNFTokenOfferID,
} = require('../dist/npm/src');

const testMap = [
  {
    currency: 'USDC',
    hex: '5553444300000000000000000000000000000000'
  },
  {
    currency: 'CORE',
    hex: '434F524500000000000000000000000000000000'
  },
  {
    currency: 'SOLO',
    hex: '534F4C4F00000000000000000000000000000000'
  },
]

describe('test convert fromCurrencyToHex & fromHexToCurrency', function () {
  it('test map', function () {
    testMap.forEach((testMap) => {
      const fromResponse = fromCurrencyToHex(testMap.currency);
      expect(fromResponse).toEqual(testMap.hex);
      const toResponse = fromHexToCurrency(testMap.hex);
      expect(toResponse == testMap.currency);
    })
  })
})

describe('test build nftokenID', function () {
  it('buildNFTokenID', function () {
    const flags = 11;
    const fee = 1337;
    const sequence = 12;
    const taxon = 1337;
    const result = buildNFTokenID(
      flags,
      fee,
      "rJoxBSzpXhPtAuqFmqxQtGKjA13jUJWthE",
      sequence,
      taxon,
    )
    expect(result).toEqual('000B0539C35B55AA096BA6D87A6E6C965A6534150DC56E5E12C5D09E0000000C');
  })
})

describe('test build offerID', function () {
  it('buildOfferID', function () {
    const account = 'rJpMn8yEHeWSQ6w581dJsk8Z2jhCUEWbwD';
    const accountSeq = 538710;
    const response = buildNFTokenOfferID(account, accountSeq);
    expect(response).toEqual('A520BF32C8CB877703D3E6E2FE71BC2FF0347A3C6A6C92092956D7E8D39ADD40');
  })
})
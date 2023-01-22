const { fromCurrencyToHex, fromHexToCurrency } = require('../dist/npm/src');

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
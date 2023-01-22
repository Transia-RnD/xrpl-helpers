
import { convertHexToString, convertStringToHex } from 'xrpl';

export const fromCurrencyToHex = (symbol: string) => {
  if (symbol.length > 3) {
    const hex = convertStringToHex(symbol.toUpperCase());
    return hex.padEnd(40, '0');
  }
  return symbol;
};

export const fromHexToCurrency = (symbol: string) => {
  if (symbol.length > 3) {
    return convertHexToString(symbol);
  }
  return symbol;
};

import { convertHexToString, convertStringToHex } from 'xrpl';

export const fromCurrencyToHex = (currency: string) => {
  if (currency.length > 3) {
    const hex = convertStringToHex(currency.toUpperCase());
    return hex.padEnd(40, '0');
  }
  return currency;
};

export const fromHexToCurrency = (hex: string) => {
  if (hex.length > 3) { return convertHexToString(hex); }
  return hex;
};
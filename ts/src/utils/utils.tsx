import { decodeAccountID } from "@transia/ripple-address-codec";
import { convertHexToString, convertStringToHex } from "@transia/xrpl";
import { createHash } from "crypto";
import BigNumber from "bignumber.js";

/**
 * convert currency to hex
 * @param currency currency string
 * @returns hex string
 */
export const fromCurrencyToHex = (currency: string): string => {
  if (currency.length > 3) {
    const hex = convertStringToHex(currency.toUpperCase());
    return hex.padEnd(40, "0");
  }
  return currency;
};

/**
 * convert hex to currency
 * @param hex hex string
 * @returns currency string
 */
export const fromHexToCurrency = (hex: string): string => {
  if (hex.length > 3) {
    return convertHexToString(hex);
  }
  return hex;
};

/**
 * unscramble taxon
 * @param taxon taxon number
 * @param token_seq token sequence number
 * @returns unscrambled taxon number
 */
function unscrambleTaxon(taxon: number, token_seq: number): number {
  return (taxon ^ (384160001 * token_seq + 2459)) % 4294967296;
}

function getLastModifiedNode(meta: Record<string, any>, ledgerEntry: string) {
  const modifiedNodes = meta.AffectedNodes.filter(
    (node) => node.ModifiedNode?.LedgerEntryType === ledgerEntry
  );
  return modifiedNodes.pop();
}

/**
 * Builds a NFToken ID from the given parameters.
 *
 * @param tx - The validated transaction including metadata
 * @returns The NFToken ID.
 */
export function buildNFTokenIDFromTx(
  tx: Record<string, any>,
  meta: Record<string, any>
): string {
  const sequence =
    getLastModifiedNode(meta, "AccountRoot").ModifiedNode.PreviousFields
      .MintedNFTokens || 0;
  const account = tx.Issuer || tx.Account;
  const flags = tx.Flags;
  const fee = tx.TransferFee;
  const taxon = tx.NFTokenTaxon;
  return buildNFTokenID(flags, fee, account, sequence, taxon);
}

/**
 * Builds a NFToken ID from the given parameters.
 *
 * @param flags - The flags for the NFToken.
 * @param fee - The fee for the NFToken.
 * @param account - The account that owns the NFToken.
 * @param sequence - The sequence number of the NFToken.
 * @param taxon - The taxon of the NFToken.
 * @returns The NFToken ID.
 */
export function buildNFTokenID(
  flags: number,
  fee: number,
  account: string,
  sequence: number,
  taxon: number
): string {
  const prefix = Buffer.alloc(1);
  const flagByteInt = Buffer.alloc(1);
  const feeByteInt = Buffer.alloc(2);
  const decodeResult = decodeAccountID(account);
  const sequenceByteInt = Buffer.alloc(4);
  const taxonByteInt = Buffer.alloc(4);

  prefix.writeUInt8(0, 0);
  flagByteInt.writeUInt8(flags, 0);
  feeByteInt.writeUInt16BE(fee, 0);
  sequenceByteInt.writeUInt32BE(sequence, 0);
  taxonByteInt.writeUInt32BE(unscrambleTaxon(taxon, sequence), 0);

  const nftokenId = Buffer.concat([
    prefix,
    flagByteInt,
    feeByteInt,
    decodeResult,
    taxonByteInt,
    sequenceByteInt,
  ]);

  return nftokenId.toString("hex").toUpperCase();
}

/**
 * Builds the NFToken Offer ID
 * @param account Account that initiated the offer tx
 * @param sequence Sequence on the offer tx
 * @returns Offer ID
 */
export function buildNFTokenOfferID(account: string, sequence: number): string {
  const decodeResult: Buffer = decodeAccountID(account);
  const sequenceByteInt = Buffer.alloc(4);
  sequenceByteInt.writeUInt32BE(sequence, 0);
  const offerBytes: Buffer = Buffer.concat([
    Buffer.from([0x00, 0x71]),
    decodeResult,
    sequenceByteInt,
  ]);
  const offerHash = createHash("sha512").update(offerBytes).digest();
  return offerHash.slice(0, 32).toString("hex").toUpperCase();
}

export function buildXrplID(
  type: number,
  subtype: number,
  hash: string,
  network: number
): string {
  const typeByteInt = Buffer.alloc(2);
  const subtypeByteInt = Buffer.alloc(2);
  const networkByteInt = Buffer.alloc(4);
  const hashBytes: Buffer = Buffer.from(hash, "hex");
  networkByteInt.writeUInt32BE(network, 0);
  typeByteInt.writeUInt16BE(type, 0);
  subtypeByteInt.writeUInt16BE(subtype, 0);
  const xrplId = Buffer.concat([
    typeByteInt,
    subtypeByteInt,
    hashBytes,
    networkByteInt,
  ]);
  return xrplId.toString("hex").toUpperCase();
}

export function parseXrplID(xrplID: string): {
  xrplID: string;
  type?: number;
  subtype?: number;
  hash: string;
  network: number;
} {
  const expectedLength = 80;
  if (xrplID.length !== expectedLength) {
    throw new Error(
      `Attempting to parse a xrplID with length ${xrplID.length}, but expected a token with length ${expectedLength}`
    );
  }
  const network = new BigNumber(xrplID.substring(72, 80), 16).toNumber();
  const XRPLID = {
    xrplID: xrplID,
    type: new BigNumber(xrplID.substring(0, 4), 16).toNumber(),
    subtype: new BigNumber(xrplID.substring(4, 8), 16).toNumber(),
    hash: xrplID.substring(8, 72),
    network: network,
  };
  return XRPLID;
}

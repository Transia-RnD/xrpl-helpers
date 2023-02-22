/**
 * @module tts
 * @description
 * This module contains the transaction types and the function to calculate the hook on
 */

const createHash = require("create-hash");

/**
 * @constant tts
 * @description
 * Transaction types
 */
export const tts = {
  ttPAYMENT: 0,
  ttESCROW_CREATE: 1,
  ttESCROW_FINISH: 2,
  ttACCOUNT_SET: 3,
  ttESCROW_CANCEL: 4,
  ttREGULAR_KEY_SET: 5,
  ttOFFER_CREATE: 7,
  ttOFFER_CANCEL: 8,
  ttTICKET_CREATE: 10,
  ttSIGNER_LIST_SET: 12,
  ttPAYCHAN_CREATE: 13,
  ttPAYCHAN_FUND: 14,
  ttPAYCHAN_CLAIM: 15,
  ttCHECK_CREATE: 16,
  ttCHECK_CASH: 17,
  ttCHECK_CANCEL: 18,
  ttDEPOSIT_PREAUTH: 19,
  ttTRUST_SET: 20,
  ttACCOUNT_DELETE: 21,
  ttHOOK_SET: 22,
  ttNFTOKEN_MINT: 25,
  ttNFTOKEN_BURN: 26,
  ttNFTOKEN_CREATE_OFFER: 27,
  ttNFTOKEN_CANCEL_OFFER: 28,
  ttNFTOKEN_ACCEPT_OFFER: 29,
};

/**
 * @typedef TTS
 * @description
 * Transaction types
 */
export type TTS = typeof tts;

/**
 * @function calculateHookOn
 * @description
 * Calculate the hook on
 * @param {(keyof TTS)[]} arr - array of transaction types
 * @returns {string} - the hook on
 */
export function calculateHookOn(arr: (keyof TTS)[]): string {
  let s = "0x3e3ff5bf";
  arr.forEach((n) => {
    let v = BigInt(s);
    v ^= BigInt(1) << BigInt(tts[n]);
    s = "0x" + v.toString(16);
  });
  s = s.replace("0x", "");
  s = s.padStart(64, "0");
  return s;
}

/**
 * @function sha256
 * @description
 * Calculate the sha256 of a string
 * @param {string} string - the string to calculate the sha256
 * @returns {string} - the sha256
 */
export const sha256 = async (string: string): Promise<string> => {
  const hash = createHash("sha256");
  hash.update(string);
  const hashBuffer = hash.digest();
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray
    .map((bytes) => bytes.toString(16).padStart(2, "0"))
    .join("");
  return hashHex;
};

/**
 * @function hexNamespace
 * @description
 * Calculate the hex of a namespace
 * @param {string} namespace - the namespace to calculate the hex
 * @returns {string} - the hex
 */
export async function hexNamespace(namespace: string): Promise<string> {
  return (await sha256(namespace)).toUpperCase();
}

/**
 * @function hexHookParameters
 * @description
 * Calculate the hex of the hook parameters
 * @param {any[]} data - the hook parameters
 * @returns {any[]} - the hex of the hook parameters
 */
export function hexHookParameters(data: any[]): any[] {
  const hookParameters: any[] = [];
  for (const parameter of data) {
    hookParameters.push({
      HookParameter: {
        HookParameterName: Buffer.from(
          parameter.HookParameter.HookParameterName,
          "utf8"
        )
          .toString("hex")
          .toUpperCase(),
        HookParameterValue: parameter.HookParameter.HookParameterValue,
      },
    });
  }
  return hookParameters;
}

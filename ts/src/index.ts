const crypto = require("crypto");

//bitbucket.org/angellenterprises/gambit-admin/src/1a81fc8c924718f0ec24d91a5e3168c4577f3d3c/server/services/xrp/contracts/liteacc/pay-from-lite.js

https: export const tts = {
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

export type TTS = typeof tts;

export function calculateHookOn(arr: (keyof TTS)[]) {
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

export const sha256 = async (string: string) => {
  const utf8 = new TextEncoder().encode(string);
  const hashBuffer = await crypto.subtle.digest("SHA-256", utf8);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray
    .map((bytes) => bytes.toString(16).padStart(2, "0"))
    .join("");
  return hashHex;
};

export async function hexNamespace(namespace: string) {
  return (await sha256(namespace)).toUpperCase();
}

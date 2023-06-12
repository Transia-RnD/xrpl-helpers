import { assert } from "chai";

import {
  Client,
  Wallet,
  type SubmitResponse,
  TimeoutError,
  NotConnectedError,
  TxResponse,
} from "@transia/xrpl";
import { Transaction } from "@transia/xrpl";
import { hashSignedTx } from "@transia/xrpl/dist/npm/utils/hashes";

export async function submitTransaction({
  client,
  transaction,
  wallet,
  retry = { count: 5, delayMs: 1000 },
}: {
  client: Client;
  transaction: Transaction;
  wallet: Wallet;
  retry?: {
    count: number;
    delayMs: number;
  };
}): Promise<SubmitResponse> {
  let response: SubmitResponse;
  try {
    response = await client.submit(transaction, { wallet });

    console.log(response);

    // Retry if another transaction finished before this one
    while (
      ["tefPAST_SEQ", "tefMAX_LEDGER"].includes(
        response.result.engine_result
      ) &&
      retry.count > 0
    ) {
      // eslint-disable-next-line no-param-reassign -- we want to decrement the count
      retry.count -= 1;
      // eslint-disable-next-line no-await-in-loop, no-promise-executor-return -- We are waiting on retries
      await new Promise((resolve) => setTimeout(resolve, retry.delayMs));
      // eslint-disable-next-line no-await-in-loop -- We are retrying in a loop on purpose
      response = await client.submit(transaction, { wallet });
    }
  } catch (error: any) {
    console.log(error);
    console.log(JSON.stringify(error.data.decoded));
    console.log(JSON.stringify(error.data.tx));

    if (error instanceof TimeoutError || error instanceof NotConnectedError) {
      // retry
      return submitTransaction({
        client,
        transaction,
        wallet,
        retry: {
          ...retry,
          count: retry.count > 0 ? retry.count - 1 : 0,
        },
      });
    }

    throw error;
  }

  return response;
}

export async function verifySubmittedTransaction(
  client: Client,
  tx: Transaction | string,
  hashTx?: string
): Promise<TxResponse> {
  const hash = hashTx ?? hashSignedTx(tx);
  const data = await client.request({
    command: "tx",
    transaction: hash,
  });

  assert(data.result);
  return data;
}

// eslint-disable-next-line max-params -- Test function, many params are needed
export async function appTransaction(
  client: Client,
  transaction: Transaction,
  wallet: Wallet,
  retry?: {
    hardFail: boolean | true;
    count: number;
    delayMs: number;
  }
): Promise<TxResponse> {
  return prodTransaction(client, transaction, wallet, retry);
}

export async function prodTransaction(
  client: Client,
  transaction: Transaction,
  wallet: Wallet,
  retry?: {
    hardFail: boolean | true;
    count: number;
    delayMs: number;
  }
): Promise<TxResponse> {
  // sign/submit the transaction
  console.log(transaction);

  const response = await client.submit(transaction, {
    autofill: true,
    wallet: wallet,
  });

  console.log(response.result.engine_result);

  // check that the transaction was successful
  assert.equal(response.type, "response");

  // check that the transaction was successful
  assert.equal(response.type, "response");

  if (response.result.engine_result !== "tesSUCCESS") {
    // eslint-disable-next-line no-console -- See output
    console.error(
      `Transaction was not successful. Expected response.result.engine_result to be tesSUCCESS but got ${response.result.engine_result}`
    );
    // eslint-disable-next-line no-console -- See output
    console.error("The transaction was: ", transaction);
    // eslint-disable-next-line no-console -- See output
    console.error("The response was: ", JSON.stringify(response));
  }

  if (retry?.hardFail) {
    assert.equal(
      response.result.engine_result,
      "tesSUCCESS",
      response.result.engine_result_message
    );
  }

  // check that the transaction is on the ledger
  return await verifySubmittedTransaction(
    client,
    "",
    response.result.tx_json.hash as string
  );
  // return response
}

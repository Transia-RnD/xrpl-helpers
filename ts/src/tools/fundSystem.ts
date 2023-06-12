import { Client, Wallet } from "@transia/xrpl";
import {
  Account,
  ICXRP,
  IC,
  fund,
  trust,
  pay,
  balance,
  limit,
  accountSet,
} from "./tools";

/**
 *
 *
 * @returns {Wallet}
 */
export async function fundSystem(
  client: Client,
  wallet: Wallet,
  ic: IC
): Promise<void> {
  // const accReserveFee = await accountReserveFee(client)
  // const ownReserveFee = await ownerReserveFee(client)

  // INIT ACCOUNTS
  const gw = new Account("gw");
  const alice = new Account("alice");
  const bob = new Account("bob");
  const carol = new Account("carol");
  // INIT IC
  const USD = ic as IC;

  // FUND GW
  if ((await balance(client, gw.wallet)) == 0) {
    // Setup GW
    await fund(client, wallet, new ICXRP(2000), ...[gw.wallet]);
    await accountSet(client, gw.wallet);
  }

  // Check Funded
  const needsFunding: Wallet[] = [];
  if ((await balance(client, gw.wallet)) < 2000) {
    needsFunding.push(gw.wallet);
  }
  if ((await balance(client, alice.wallet)) < 2000) {
    needsFunding.push(alice.wallet);
  }
  if ((await balance(client, bob.wallet)) < 2000) {
    needsFunding.push(bob.wallet);
  }
  if ((await balance(client, carol.wallet)) < 2000) {
    needsFunding.push(carol.wallet);
  }

  // Check Trustline
  const needsLines: Wallet[] = [];
  if ((await limit(client, alice.wallet, USD)) < 20000) {
    needsLines.push(alice.wallet);
  }
  if ((await limit(client, bob.wallet, USD)) < 20000) {
    needsLines.push(bob.wallet);
  }
  if ((await limit(client, carol.wallet, USD)) < 20000) {
    needsLines.push(carol.wallet);
  }
  // Check IC Balance
  const needsIC: Wallet[] = [];
  if ((await balance(client, alice.wallet, USD)) < 20) {
    needsIC.push(alice.wallet);
  }
  if ((await balance(client, bob.wallet, USD)) < 20) {
    needsIC.push(bob.wallet);
  }
  if ((await balance(client, carol.wallet, USD)) < 20) {
    needsIC.push(carol.wallet);
  }

  await fund(client, wallet, new ICXRP(2000), ...needsFunding);
  await trust(client, USD.set(100000), ...needsLines);
  await pay(client, USD.set(2000), gw.wallet, ...needsIC);
}

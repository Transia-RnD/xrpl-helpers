const {
  calculateHookOn,
  hexNamespace,
  hexHookParameters,
} = require("../../dist/npm/src");

const fs = require("fs");

describe("test hook binary", function () {
  it("all", function () {
    const binary = fs
      .readFileSync("test/fixtures/starter.c.wasm")
      .toString("hex")
      .toUpperCase();
    expect(binary).toEqual(
      "0061736D01000000011C0460057F7F7F7F7F017E60037F7F7E017E60027F7F017F60017F017E02230303656E76057472616365000003656E7606616363657074000103656E76025F670002030201030503010002062B077F0141B088040B7F004180080B7F0041A6080B7F004180080B7F0041B088040B7F0041000B7F0041010B07080104686F6F6B00030AC4800001C0800001017F230041106B220124002001200036020C41920841134180084112410010001A410022002000420010011A41012200200010021A200141106A240042000B0B2C01004180080B254163636570742E633A2043616C6C65642E00224163636570742E633A2043616C6C65642E22"
    );
  });
});

describe("test hook on", function () {
  it("invalid", function () {
    const invokeOn = ["AccountSet1"];
    expect(() => {
      calculateHookOn(invokeOn);
    }).toThrow("invalid transaction type array");
  });
  it("all", function () {
    const result = calculateHookOn([]);
    expect(result).toEqual(
      "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFFF"
    );
  });
  it("one", function () {
    const invokeOn = ["AccountSet"];
    const result = calculateHookOn(invokeOn);
    expect(result).toEqual(
      "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFF7"
    );
  });
});

describe("test hook namespace", function () {
  it("basic", async function () {
    const result = await hexNamespace("starter");
    expect(result).toEqual(
      "4FF9961269BF7630D32E15276569C94470174A5DA79FA567C0F62251AA9A36B9"
    );
  });
});

describe("test hook parameters", function () {
  it("basic", async function () {
    const parameters = [
      {
        HookParameter: {
          HookParameterName: "name1",
          HookParameterValue: "value1",
        },
      },
    ];
    const result = hexHookParameters(parameters);
    expect(result).toEqual([
      {
        HookParameter: {
          HookParameterName: "6E616D6531",
          HookParameterValue: "76616C756531",
        },
      },
    ]);
  });
});

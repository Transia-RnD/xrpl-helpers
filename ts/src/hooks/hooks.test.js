const {
  calculateHookOn,
  hexNamespace,
  hexHookParameters,
} = require("../../dist/npm/src");

describe("test hook on", function () {
  it("all", function () {
    const result = calculateHookOn([]);
    expect(result).toEqual(
      "000000000000000000000000000000000000000000000000000000003e3ff5bf"
    );
  });
  it("one", function () {
    const invokeOn = ["ttACCOUNT_SET"];
    const result = calculateHookOn(invokeOn);
    expect(result).toEqual(
      "000000000000000000000000000000000000000000000000000000003e3ff5b7"
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
          HookParameterValue: "value1",
        },
      },
    ]);
  });
});

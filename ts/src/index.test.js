const { calculateHookOn, hexNamespace } = require("../dist/npm/src");

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
  it("basic", function () {
    const result = hexNamespace("starter");
    expect(result).toEqual(
      "000000000000000000000000000000000000000000000000000000003e3ff5bf"
    );
  });
});

import { useNetwork } from "wagmi";
import { constants, utils } from "ethers";

import networkMapping from "../chain-info/map.json";

import contract1 from "../chain-info/MultiSigWallet.json";
import contract2 from "../chain-info/TestContract.json";

const useGetContract = (contractName) => {
  const { activeChain } = useNetwork();
  let contractAddress;

  if (!networkMapping[String(activeChain?.id)]) {
    contractAddress = constants.AddressZero;
  } else {
    contractAddress = activeChain?.id
      ? networkMapping[String(activeChain.id)][contractName][0]
      : constants.AddressZero;
  }

  const { abi: abiContract1 } = contract1;
  const { abi: abiContract2 } = contract2;

  const formattedAddress = utils.getAddress(contractAddress);

  if (contractName === "MultiSigWallet") {
    return {
      address: activeChain ? formattedAddress : constants.AddressZero,
      ABI: abiContract1,
    };
  }
  if (contractName === "TestContract") {
    return {
      address: activeChain ? formattedAddress : constants.AddressZero,
      ABI: abiContract2,
    };
  }

  return { address: formattedAddress, ABI: abiContract1 };
};

export default useGetContract;

import { useNetwork } from "wagmi";
import { constants } from "ethers";

import contractJson from "../chain-info/MultiSigWallet.json";
import networkMapping from "../chain-info/map.json";

const GetContract = (contractName) => {
  const { activeChain } = useNetwork();
  let contractAddress;

  if (!networkMapping[String(activeChain?.id)]) {
    contractAddress = constants.AddressZero;
  } else {
    contractAddress = activeChain?.id
      ? networkMapping[String(activeChain.id)][contractName][0]
      : constants.AddressZero;
  }

  const { abi } = contractJson;
  if (!activeChain)
    return { contractAddress: constants.AddressZero, contractABI: abi };

  return { contractAddress: contractAddress, contractABI: abi };
};

export default GetContract;
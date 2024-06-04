import React from "react";
import { Select, SelectItem } from "@tremor/react";

import { useAtom } from "jotai";
import { ensemblesAtom, currEnsembleAtom } from "@/atoms/atoms";

const EnsembleSelect = () => {
    const [ensembles, setEnsembles] = useAtom(ensemblesAtom);
    const [currEnsemble, setCurrEnsemble] = useAtom(currEnsembleAtom);

    return (
        <Select
            defaultValue="None"
            placeholder={`Select Ensemble`}
            enableClear={false}
            className="w-[190px]"
        >
            {ensembles.map((ensemble: any) => {
                return (
                    <SelectItem
                        key={ensemble.id}
                        value={ensemble.id}
                        onClick={() => setCurrEnsemble(ensemble)}
                    >
                        {`${ensemble.ensembleName} (${ensemble.numberOfPlans} Plans)`}
                    </SelectItem>
                );
            })}
        </Select>
    );
};

export default EnsembleSelect;

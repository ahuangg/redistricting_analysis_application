import React from "react";
import { Select, SelectItem } from "@tremor/react";
import { MEASURE_OPTIONS } from "@/constants/stringConstants";

import { useAtom } from "jotai";
import { currClusterAtom, currEnsembleAtom, currStateAtom, districtPlansAtom, loadingAtom, measureAtom, pageStateAtom } from "@/atoms/atoms";

const MeasureSelect = () => {
    const [currState, setCurrState] = useAtom(currStateAtom);
    const [measure, setMeasure] = useAtom(measureAtom);
    const [currCluster, setCurrCluster] = useAtom(currClusterAtom);
    const [districtPlans, setDistrictPlans] = useAtom(districtPlansAtom);
    const [pageState, setPageState] = useAtom(pageStateAtom);
    const [currEnsemble, setCurrEnsemble] = useAtom(currEnsembleAtom);

    return (
        <Select
            defaultValue=""
            placeholder="Select Scatter Plot" 
            className="w-[690px]"
            value={measure}
            disabled={Object.keys(currEnsemble).length === 0 ? true : false}
            onValueChange={(value) => {
                setCurrCluster({});
                setDistrictPlans([]);
                if (value === "") {
                    setMeasure("");
                    setPageState("OverView");
                } else {
                    setMeasure(value);
                }
            }}
        >
            {MEASURE_OPTIONS[currState].map((measure: string) => {
                return (
                    <SelectItem
                        key={measure}
                        value={measure}
                        onClick={() => {setMeasure(measure);}}
                    >
                        {measure}
                    </SelectItem>
                );
            })}
        </Select>
    );
};

export default MeasureSelect;

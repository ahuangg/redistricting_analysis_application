import React from "react";
import { Col, Card, Text, ScatterChart, Button } from "@tremor/react";
import { MEASURE_LABELS } from "@/constants/stringConstants";

import { useAtom } from "jotai";
import {
    measureAtom,
    districtPlansAtom,
    currClusterAtom,
    currDistrictPlanAtom,
    boundaryAtom,
} from "@/atoms/atoms";
import { formatPlansScatterData } from "@/utils/format";

import { fetchBoundary } from "@/utils/fetch";

const DistrictPlansScatterGraph = () => {
    const [measure, setMeasure] = useAtom(measureAtom);
    const [districtPlans, setDistrictPlans] = useAtom(districtPlansAtom);
    const [currCluster, setCurrCluster] = useAtom(currClusterAtom);
    const [currDistrictPlan, setCurrDistrictPlan] =
        useAtom(currDistrictPlanAtom);
    const [boundary, setBoundary] = useAtom(boundaryAtom);

    let plansScatterData: any[] = formatPlansScatterData(districtPlans);

    React.useEffect(() => {
        plansScatterData = formatPlansScatterData(districtPlans);
    }, [districtPlans]);

    const valueFormatter = {
        x: (x: any) => `${x} ${MEASURE_LABELS[measure]["xUnit"]}`,
        y: (y: any) => `${y} ${MEASURE_LABELS[measure]["yUnit"]}`,
    };

    return (
        <Card className="p-2 shadow-lg">
            <Text className="font-extrabold text-lg pl-1">{measure}</Text>
            <Col className="flex">
                <Col className="flex justify-center items-center flex-shrink-0 w-[30px]">
                    <Col className="font-bold transform -rotate-90">
                        <Text className="font-bold p-1">
                            {MEASURE_LABELS[measure]["yLabel"].replace(
                                / /g,
                                "\v\v"
                            )}
                        </Text>
                    </Col>
                </Col>

                <Col className="flex flex-col flex-grow">
                    <Col className="flex-grow ">
                        <ScatterChart
                            className="p-1 -ml-6 pl-0 h-[380px]"
                            minYValue={0}
                            yAxisWidth={100}
                            data={plansScatterData}
                            category={"availability"}
                            colors={["blue", "red"]}
                            size={"planSize"}
                            x={MEASURE_LABELS[measure]["xLabel"]}
                            y={MEASURE_LABELS[measure]["yLabel"]}
                            showOpacity={false}
                            showLegend={true}
                            allowDecimals={false}
                            valueFormatter={valueFormatter}
                            onValueChange={(v) => {
                                if (v == undefined) {
                                    return;
                                }
                                setCurrDistrictPlan(v);
                                fetchBoundary(v.boundaryId, setBoundary);
                            }}
                            autoMinYValue={true}
                            autoMinXValue={true}
                        />
                    </Col>

                    <Col className="flex justify-center items-center text-center relative">
                        <Text className="font-bold">
                            {MEASURE_LABELS[measure]["xLabel"]}
                        </Text>
                        <Button
                            className="py-.5 px-2 justify-right absolute bottom-0 right-0"
                            onClick={() => {
                                setDistrictPlans([]);
                                setCurrCluster({});
                            }}
                        >
                            Back
                        </Button>
                    </Col>
                </Col>
            </Col>
        </Card>
    );
};

export default DistrictPlansScatterGraph;

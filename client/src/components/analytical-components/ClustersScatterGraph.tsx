import React from "react";
import { Col, Card, Text, ScatterChart, Button } from "@tremor/react";
import { MEASURE_LABELS } from "@/constants/stringConstants";

import { useAtom } from "jotai";
import {
    measureAtom,
    clustersAtom,
    districtPlansAtom,
    currClusterAtom,
} from "@/atoms/atoms";
import { formatClustersScatterData } from "@/utils/format";
import { fetchDistrictPlans } from "@/utils/fetch";

const ClustersScatterGraph = () => {
    const [measure, setMeasure] = useAtom(measureAtom);
    const [clusters, setClusters] = useAtom(clustersAtom);
    const [districtPlans, setDistrictPlans] = useAtom(districtPlansAtom);
    const [currCluster, setCurrCluster] = useAtom(currClusterAtom);

    let clustersScatterData: any[] = formatClustersScatterData(clusters);

    React.useEffect(() => {
        clustersScatterData = formatClustersScatterData(clusters);
    }, [clusters]);

    const valueFormatter = {
        x: (x: any) => `${x} ${MEASURE_LABELS[measure]["xUnit"]}`,
        y: (y: any) => `${y} ${MEASURE_LABELS[measure]["yUnit"]}`,
    };

    return (
        <Card className="p-2 h-[438px] shadow-lg">
            {measure === "" || MEASURE_LABELS[measure] == undefined ? (
                <Text className="text-center">Select a Measure to View</Text>
            ) : (
                <React.Fragment>
                    <Text className="font-extrabold text-lg pl-1">
                        {measure}
                    </Text>
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
                                    yAxisWidth={100}
                                    data={clustersScatterData}
                                    category={"Cluster"}
                                    colors={Array(100).fill("blue")}
                                    x={MEASURE_LABELS[measure]["xLabel"]}
                                    y={MEASURE_LABELS[measure]["yLabel"]}
                                    size={"numberOfPlans"}
                                    showOpacity={false}
                                    showLegend={false}
                                    allowDecimals={false}
                                    valueFormatter={valueFormatter}
                                    onValueChange={(v) => {
                                        setCurrCluster(v);
                                        fetchDistrictPlans(
                                            v.districtPlanIds,
                                            setDistrictPlans
                                        );
                                    }}
                                    autoMinYValue={true}
                                    autoMinXValue={true}
                                />
                            </Col>
                            <Col className="flex justify-center items-center text-center relative">
                                <Text className="font-bold">
                                    {MEASURE_LABELS[measure]["xLabel"]}
                                </Text>
                            </Col>
                        </Col>
                    </Col>
                </React.Fragment>
            )}
        </Card>
    );
};

export default ClustersScatterGraph;

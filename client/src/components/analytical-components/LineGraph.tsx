import React from "react";
import { Col, Card, Text, LineChart } from "@tremor/react";

import { useAtom } from "jotai";
import { currEnsembleAtom, currStateAtom } from "@/atoms/atoms";

const valueFormatter = (number: number) =>
    `${new Intl.NumberFormat("us").format(number).toString()}`;

const LineGraph = () => {
    const [currEnsemble, setCurrEnsemble] = useAtom(currEnsembleAtom);
    const [currState, setCurrState] = useAtom(currStateAtom);

    return (
        <Card className="p-1 shadow-lg h-[434px]">
            <Text className="font-extrabold text-lg pl-1">
                {`Ensemble Size vs. Number of Clusters for ${currState}`}
            </Text>
            {currEnsemble.ensembleClusterSizeAssociation === undefined ? (
                <Text className="text-center">Select Ensemble to View</Text>
            ) : (
                <React.Fragment>
                    <Col className="flex">
                        <Col className="flex justify-center items-center flex-shrink-0 w-[30px]">
                            <Col className="font-bold transform -rotate-90">
                                <Text className="font-bold">
                                    {"Cluster\v\vSize"}
                                </Text>
                            </Col>
                        </Col>

                        <Col className="flex flex-col flex-grow">
                            <Col className="flex-grow ">
                                <LineChart
                                    className="mt-6"
                                    data={
                                        currEnsemble.ensembleClusterSizeAssociation
                                    }
                                    index="ensembleSize"
                                    categories={["numberOfClusters"]}
                                    colors={["blue"]}
                                    valueFormatter={valueFormatter}
                                    yAxisWidth={40}
                                    showLegend={false}
                                />
                            </Col>

                            <Col className="flex justify-center">
                                <Text className="font-bold">Ensemble Size</Text>
                            </Col>
                        </Col>
                    </Col>
                </React.Fragment>
            )}
        </Card>
    );
};

export default LineGraph;

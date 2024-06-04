import React from "react";
import { Card, Col, Icon, Button, Text } from "@tremor/react";
import { ArrowPathIcon } from "@heroicons/react/24/outline";
import StateSelect from "./StateSelect";

import { TEAM_NAME, PLAN_TYPE } from "@/constants/stringConstants";

import { useSetAtom, useAtomValue } from "jotai";
import {
    currStateAtom,
    currEnsembleAtom,
    measureAtom,
    pageStateAtom,
} from "@/atoms/atoms";

import EnsembleSelect from "@/components/general-components/EnsembleSelect";
import MeasureSelect from "@/components/general-components/MeasureSelect";

const Header = () => {
    const currState = useAtomValue(currStateAtom);
    const currEnsemble = useAtomValue(currEnsembleAtom);
    const measure = useAtomValue(measureAtom);
    const setPageState = useSetAtom(pageStateAtom);

    return (
        <Col className="p-2 px-1 w-full flex justify-between items-center">
            <Col className="flex justify-center items-center">
                <h3 className="text-2xl mx-3 font-medium">{TEAM_NAME}</h3>
                <StateSelect />
                <Text className="font-extrabold text-lg pl-2">
                    {PLAN_TYPE[currState]}
                </Text>
            </Col>
            {currState === "All States" ? null : (
                <Card className="flex p-0.5 w-[960px] justify-between bg-slate-100">
                    <EnsembleSelect /> <MeasureSelect />
                    <Button
                        size="xs"
                        disabled={currEnsemble === "" || measure === ""}
                        onClick={() => {
                            setPageState("DetailedView");
                        }}
                    >
                        Plot
                    </Button>
                </Card>
            )}
            <Icon
                icon={ArrowPathIcon}
                size="md"
                tooltip="Refresh Page"
                className="mr-3 hover:opacity-60 cursor-pointer"
                variant="shadow"
                onClick={() => {
                    window.location.reload();
                }}
            />
        </Col>
    );
};

export default Header;

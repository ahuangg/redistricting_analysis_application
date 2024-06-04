"use client";

import React from "react";
import { Col } from "@tremor/react";
import Header from "@/components/general-components/Header";
import { handlePageState } from "@/utils/handlePageState";

import { useAtomValue } from "jotai";
import { pageStateAtom } from "@/atoms/atoms";

const page = () => {
    const pageState = useAtomValue(pageStateAtom);

    return (
        <React.Fragment>
            <Header />
            <Col className="px-3">{handlePageState(pageState)}</Col>
        </React.Fragment>
    );
};

export default page;

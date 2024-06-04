export const TEAM_NAME: string = "Baltimore Ravens";

export const states: string[] = [
    "All States",
    "North Carolina",
    "Texas",
    "Pennsylvania",
];

interface Map {
    [index: string]: string;
}

export const PLAN_TYPE: Map = {
    "All States": "All State Boundaries",
    "North Carolina": "2022 Federal Congressional District Plan",
    Texas: "2022 Federal Congressional District Plan",
    Pennsylvania: "2022 Federal Congressional District Plan",
};

export const MEASURE_OPTIONS: any = {
    "All States": [],
    "North Carolina": [
        "MDS_X vs MDS_Y",
        "Median R/D split vs Average Opportunity Districts for Black(>30.0%)",
    ],
    Texas: [
        "MDS_X vs MDS_Y",
        "Median R/D split vs Average Opportunity Districts for Black(>30.0%)",
    ],
    Pennsylvania: [
        "MDS_X vs MDS_Y",
        "Median R/D split vs Average Opportunity Districts for Black(>30.0%)",
    ],
};

export const MEASURE_LABELS: any = {
    "Median R/D split vs Average Opportunity Districts for Black(>30.0%)": {
        xLabel: "Median R/D split",
        xUnit: "%",
        yLabel: "Average Opportunity Districts for Black(>30.0%)",
        yUnit: "Districts",
        size: "Cluster Size",
    },
    "MDS_X vs MDS_Y": {
        xLabel: "MDS_X",
        xUnit: "",
        yLabel: "MDS_Y",
        yUnit: "",
        size: "Cluster Size",
    },
};

export const DISTANCE_HEADER = [
    "min",
    "Q1",
    "median",
    "Q3",
    "max",
    "average",
    "optimality",
    "timeToRun",
];

export const ENSEMBLE_HEADER = ["clusterName", "numberOfPlans"];

export const DISTRICT_PLAN_HEADER = ["districtPlanName", "availability"];

export const MEASURE_HEADER = [
    "Average Opportunity Districts for Black(>30.0%)",
    "Median R/D split",
    "MDS_X",
    "MDS_Y",
];

export const DISTRICT_PLAN_MEASURE_HEADER = [
    "Average Opportunity Districts for Black(>30.0%)",
    "Median R/D split",
    "R",
    "D",
    "MDS_X",
    "MDS_Y",
];

export const HEADER_MAPPING: any = {
    clusterId: "Cluster Id",
    clusterName: "Cluster Name",
    numberOfPlans: "# of Plans",
    districtPlanId: "Plan Id",
    districtPlanName: "Plan Name",
    availability: "Availability",
    "Average Opportunity Districts for Black(>30.0%)":
        "Avg Opp Dist for Black>30.0%",
    "Median R/D split": "Avg R/D split",
    MDS_X: "MDS_X",
    MDS_Y: "MDS_Y",
    R: "R",
    D: "D",
};

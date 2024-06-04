import { atom } from "jotai";

const pageStateAtom = atom<string>("MapView");

const currStateAtom = atom<string>("All States");

const stateAtom = atom<any>({});

const boundaryAtom = atom<any>({});

const loadingAtom = atom<boolean>(false);

const ensemblesAtom = atom<any>([]);

const currEnsembleAtom = atom<any>({});

const clustersAtom = atom<any>([]);

const currClusterAtom = atom<any>({});

const districtPlansAtom = atom<any>([]);

const measureAtom = atom<string>("");

const currDistrictPlanAtom = atom<any>({});

const districtPlanBoundaryAtom = atom<any>({});

export {
    pageStateAtom,
    currStateAtom,
    stateAtom,
    boundaryAtom,
    loadingAtom,
    ensemblesAtom,
    currEnsembleAtom,
    clustersAtom,
    currClusterAtom,
    districtPlansAtom,
    measureAtom,
    currDistrictPlanAtom,
    districtPlanBoundaryAtom,
};

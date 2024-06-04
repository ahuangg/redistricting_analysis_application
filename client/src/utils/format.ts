export const formatClustersScatterData = (clusters: any) => {
    const clusterScatterData: any[] = [];
    clusters.forEach((cluster: any) => {
        clusterScatterData.push({
            clusterId: cluster.clusterId,
            numberOfPlans: cluster.numberOfPlans,
            districtPlanIds: cluster.districtPlanIds,
            ...cluster.measureData,
        });
    });
    return clusterScatterData;
};

export const formatPlansScatterData = (districtPlans: any) => {
    const plansScatterData: any[] = [];
    districtPlans.forEach((plan: any) => {
        plansScatterData.push({
            districtPlanId: plan.districtPlanId,
            planSize: 1,
            availability: plan.availability ? "Available" : "Unavailable",
            boundaryId: plan.boundaryId,
            ...plan.measureData,
        });
    });
    return plansScatterData;
};


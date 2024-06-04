package com.raven.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import com.raven.model.DistrictPlan;

public interface DistrictPlanRepository extends MongoRepository<DistrictPlan, String>{ 
	public DistrictPlan findByDistrictPlanId(int districtPlanId);
}

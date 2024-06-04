package com.raven.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor

@Document(collection = "districtplan")
public class DistrictPlan {
	@Id
	private String id;
	
	@Field("id")
	private int districtPlanId;

	@Field("name")
	private String districtPlanName;

	private boolean availability;	

	private Object measureData;

	@Field("boundaryID")
	private int boundaryId;
}

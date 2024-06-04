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

@Document(collection = "cluster")
public class Cluster {
	@Id
	private String id;
	
	private int clusterId;

	private String clusterName;

	private int numberOfPlans;

	@Field("districtPlanIDs")
	private int[] districtPlanIds;	

	private Object measureData;

}

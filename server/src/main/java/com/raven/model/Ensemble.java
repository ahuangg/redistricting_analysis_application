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

@Document(collection = "ensemble")
public class Ensemble {
	@Id
	private String id;
	
	@Field("id")
	private int ensembleId;

	private String ensembleName;

	private int numberOfPlans;

	@Field("clusterIDs")
	private int[] clusterIds;	

	private Object distanceMeasureResults;

	private Object[] ensembleClusterSizeAssociation;
}

package com.raven.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import com.raven.model.Cluster;

public interface ClusterRepository extends MongoRepository<Cluster, String>{ 
	public Cluster findByClusterId(int clusterId);
}

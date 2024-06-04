package com.raven.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import com.raven.model.Ensemble;

public interface EnsembleRepository extends MongoRepository<Ensemble, String>{ 
	public Ensemble findByEnsembleId(int ensembleId);
}

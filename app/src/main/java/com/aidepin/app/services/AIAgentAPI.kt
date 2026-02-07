package com.aidepin.app.services

import retrofit2.Response
import retrofit2.http.*

/**
 * AIAgentAPI - واجهة API للوكيل الذكي
 */
interface AIAgentAPI {

    @POST("agent/execute")
    suspend fun executeCommand(
        @Body command: Map<String, String>
    ): Response<Any>

    @GET("agent/project/{id}")
    suspend fun getProjectStatus(
        @Path("id") projectId: String
    ): Response<Any>

    @GET("agent/projects")
    suspend fun getAllProjects(
        @Query("user_id") userId: String
    ): Response<Any>

    @POST("agent/project/{id}/fix")
    suspend fun fixProjectErrors(
        @Path("id") projectId: String
    ): Response<Any>

    @POST("depin/node/register")
    suspend fun registerNode(
        @Body nodeData: Map<String, Any>
    ): Response<Any>

    @POST("depin/task/submit")
    suspend fun submitTask(
        @Body taskData: Map<String, Any>
    ): Response<Any>

    @GET("depin/task/{id}")
    suspend fun getTaskStatus(
        @Path("id") taskId: String
    ): Response<Any>

    @GET("depin/stats")
    suspend fun getNetworkStats(): Response<Any>

    @GET("depin/nodes")
    suspend fun getNodesList(): Response<Any>

    @GET("stats")
    suspend fun getStats(): Response<Any>

    @GET("health")
    suspend fun healthCheck(): Response<Any>
}

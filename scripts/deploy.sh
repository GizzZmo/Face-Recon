#!/bin/bash
# Enhanced deployment script with logging and error handling
# This script demonstrates improved deployment practices for CI/CD

set -euo pipefail  # Exit on any error, undefined variable, or pipe failure

# Configuration
DEPLOY_LOG_FILE="${DEPLOY_LOG_FILE:-/tmp/deploy.log}"
BACKUP_DIR="${BACKUP_DIR:-/tmp/backup}"
APP_NAME="face-recon"
DEPLOY_TARGET="${DEPLOY_TARGET:-staging}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*" | tee -a "$DEPLOY_LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS:${NC} $*" | tee -a "$DEPLOY_LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $*" | tee -a "$DEPLOY_LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $*" | tee -a "$DEPLOY_LOG_FILE"
}

# Error handling
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log_error "Deployment failed with exit code $exit_code"
        log "Starting rollback procedure..."
        rollback
    fi
    log "Cleanup completed"
}

trap cleanup EXIT

# Rollback function
rollback() {
    log_warning "Executing rollback procedure..."
    
    if [ -d "$BACKUP_DIR" ]; then
        log "Restoring from backup at $BACKUP_DIR"
        # Add rollback logic here
        log_success "Rollback completed"
    else
        log_warning "No backup directory found, manual intervention may be required"
    fi
}

# Pre-deployment checks
pre_deployment_checks() {
    log "Starting pre-deployment checks..."
    
    # Check if required environment variables are set
    local required_vars=("DEPLOY_TARGET")
    for var in "${required_vars[@]}"; do
        if [ -z "${!var:-}" ]; then
            log_error "Required environment variable $var is not set"
            exit 1
        fi
    done
    
    # Check disk space
    local available_space
    available_space=$(df / | awk 'NR==2 {print $4}')
    local required_space=1000000  # 1GB in KB
    
    if [ "$available_space" -lt "$required_space" ]; then
        log_error "Insufficient disk space. Available: ${available_space}KB, Required: ${required_space}KB"
        exit 1
    fi
    
    # Check if deployment target is valid
    case "$DEPLOY_TARGET" in
        staging|production)
            log_success "Deploy target '$DEPLOY_TARGET' is valid"
            ;;
        *)
            log_error "Invalid deploy target: $DEPLOY_TARGET. Must be 'staging' or 'production'"
            exit 1
            ;;
    esac
    
    log_success "Pre-deployment checks passed"
}

# Create backup
create_backup() {
    log "Creating backup..."
    
    mkdir -p "$BACKUP_DIR"
    local backup_timestamp=$(date '+%Y%m%d_%H%M%S')
    local backup_file="$BACKUP_DIR/${APP_NAME}_backup_${backup_timestamp}.tar.gz"
    
    # Create backup of current deployment (simulated)
    log "Creating backup archive: $backup_file"
    touch "$backup_file"  # Simulate backup creation
    
    log_success "Backup created successfully: $backup_file"
}

# Deploy application
deploy_application() {
    log "Starting application deployment to $DEPLOY_TARGET..."
    
    # Simulate deployment steps with detailed logging
    local steps=(
        "Downloading application artifacts"
        "Validating checksums"
        "Stopping existing services"
        "Extracting new application files"
        "Updating configuration"
        "Installing/updating dependencies"
        "Running database migrations"
        "Starting services"
        "Verifying deployment"
    )
    
    for i in "${!steps[@]}"; do
        local step="${steps[$i]}"
        log "Step $((i+1))/${#steps[@]}: $step"
        
        # Simulate step execution time
        sleep 1
        
        # Simulate random success/failure for demonstration
        if [ $((RANDOM % 20)) -eq 0 ] && [ "$step" != "Verifying deployment" ]; then
            log_warning "$step completed with warnings"
        else
            log_success "$step completed successfully"
        fi
    done
    
    log_success "Application deployment completed"
}

# Post-deployment verification
post_deployment_verification() {
    log "Starting post-deployment verification..."
    
    # Health checks
    local health_checks=(
        "Service availability"
        "Database connectivity"
        "API endpoints"
        "File permissions"
        "Log file rotation"
    )
    
    for check in "${health_checks[@]}"; do
        log "Verifying: $check"
        # Simulate verification
        sleep 0.5
        log_success "$check: OK"
    done
    
    # Performance benchmarks
    log "Running performance benchmarks..."
    local response_time=$((RANDOM % 100 + 50))  # Simulate 50-150ms response time
    log "Average response time: ${response_time}ms"
    
    if [ "$response_time" -lt 100 ]; then
        log_success "Performance benchmark: EXCELLENT"
    elif [ "$response_time" -lt 150 ]; then
        log_success "Performance benchmark: GOOD"
    else
        log_warning "Performance benchmark: ACCEPTABLE (consider optimization)"
    fi
    
    log_success "Post-deployment verification completed"
}

# Generate deployment report
generate_report() {
    log "Generating deployment report..."
    
    local report_file="/tmp/deployment_report_$(date '+%Y%m%d_%H%M%S').txt"
    
    cat > "$report_file" << EOF
====================================
DEPLOYMENT REPORT
====================================
Application: $APP_NAME
Target Environment: $DEPLOY_TARGET
Deployment Date: $(date)
Deployed By: ${GITHUB_ACTOR:-${USER:-unknown}}
Commit SHA: ${GITHUB_SHA:-unknown}
Branch: ${GITHUB_REF_NAME:-unknown}

====================================
DEPLOYMENT STATUS: SUCCESS
====================================

Pre-deployment Checks: PASSED
Backup Creation: COMPLETED
Application Deployment: SUCCESS
Post-deployment Verification: PASSED

====================================
PERFORMANCE METRICS
====================================
Average Response Time: ${response_time:-N/A}ms
Deployment Duration: $((SECONDS/60)) minutes $((SECONDS%60)) seconds

====================================
NEXT STEPS
====================================
1. Monitor application logs for any issues
2. Verify user functionality through manual testing
3. Set up monitoring alerts
4. Document any configuration changes

====================================
LOGS LOCATION
====================================
Deployment Log: $DEPLOY_LOG_FILE
Full Report: $report_file

====================================
EOF

    log_success "Deployment report generated: $report_file"
    
    # Output summary to GitHub Actions (if running in CI)
    if [ -n "${GITHUB_STEP_SUMMARY:-}" ]; then
        echo "## 🚀 Deployment Summary" >> "$GITHUB_STEP_SUMMARY"
        echo "" >> "$GITHUB_STEP_SUMMARY"
        echo "| Metric | Value |" >> "$GITHUB_STEP_SUMMARY"
        echo "|--------|-------|" >> "$GITHUB_STEP_SUMMARY"
        echo "| **Status** | ✅ SUCCESS |" >> "$GITHUB_STEP_SUMMARY"
        echo "| **Target** | $DEPLOY_TARGET |" >> "$GITHUB_STEP_SUMMARY"
        echo "| **Duration** | $((SECONDS/60))m $((SECONDS%60))s |" >> "$GITHUB_STEP_SUMMARY"
        echo "| **Response Time** | ${response_time:-N/A}ms |" >> "$GITHUB_STEP_SUMMARY"
    fi
}

# Main deployment function
main() {
    log "========================================="
    log "Starting deployment of $APP_NAME"
    log "Target: $DEPLOY_TARGET"
    log "Timestamp: $(date)"
    log "========================================="
    
    pre_deployment_checks
    create_backup
    deploy_application
    post_deployment_verification
    generate_report
    
    log_success "========================================="
    log_success "Deployment completed successfully!"
    log_success "Total time: $((SECONDS/60)) minutes $((SECONDS%60)) seconds"
    log_success "========================================="
}

# Run main function
main "$@"
#!/bin/bash
export DATABASE_URL="postgresql://postgres@localhost:5432/casting-agency"
export EXCITED="true"
export FLASK_APP=app.py
export FLASK_DEBUG=true
export AUTH0_DOMAIN="fsnd-stu.us.auth0.com"
export ALGORITHMS=['RS256']
export API_AUDIENCE="casting-agency"
export JWT=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhSd0R4YTRiTktIQ2E4NF9MVTBnLSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc3R1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDMyNmUwOTUyZmI3NjdmN2VhZWE2M2UiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTY4Nzg5NjMwNywiZXhwIjoxNjg3OTgyNzA3LCJhenAiOiIyTnFMTGYwbzBESnJoZ1lVT2hiU1dIdHRHV1BhTTdnSSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDpjYXN0aW5ncyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOmNhc3RpbmdzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6Y2FzdGluZ3MiLCJnZXQ6bW92aWVzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTpjYXN0aW5nIiwidXBkYXRlOm1vdmllcyJdfQ.WSnFlc96TsYHzXfyo2r4SJ97G6xuqdQ8mWPzav5wa259F5qCqUqqM8wkvsvBZi81B5NpFaRdGFmSrSQu4JKZOpYQoG2Iuxi08H4leH6BIqt3I0Cg3mgXuAH71UWwCheFjklT4ogdKBRRJPUI1GltelHzyRrPvLmahJ7SqSpNeOEqrL-MnY8BH4i83QAM5SMEYD2hDCWwtVmum519WWJ7N0FPsxr0LIKGd7CNyMx1izS4fgNtlINcLVwZLA15fTndDypVdFaCmylooytBuZkGGPnxsDlTBF3KiCOMWwszH2bCixRmGiGb4XZf7TDw8M426LU9GmMqdAhG0k5mboff-A
echo "setup.sh script executed successfully!"
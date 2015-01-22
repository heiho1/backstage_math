from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.views.generic import View, TemplateView
from django.template.loader import render_to_string
import neo4j


CREATE_FORMAT = "CREATE (n:Differential {number:%s, count:1})"
UPDATE_FORMAT = "MATCH (n:Differential {number:%s}) SET n.count = %s RETURN n"
MATCH_FORMAT = "MATCH (n:Differential {number:%s}) RETURN n"

class DifferentialHome(View):
    template_name = "difference.html"
    def get(self, request):
        return HttpResponse(render_to_string("difference.html", {}))
        

class DifferentialView(View):
    def get(self, request):
        numToCalculate = int(request.GET.get('number'))
        assert numToCalculate > 0 and numToCalculate <= 100
        summationRange = range(1,numToCalculate + 1)
        sumOfSquares = self.sumOfSquares(summationRange)
        squareOfSums = self.squareOfSums(summationRange)
        jsonDict = {'datetime': datetime.now().ctime(),
            'value': abs(sumOfSquares - squareOfSums),
            'number': numToCalculate, 
            'occurrences': self.determineOccurrence(numToCalculate)}
        return JsonResponse(jsonDict)
        
    def sumOfSquares(self, aRange):
        return sum(x*x for x in aRange)
    
    def squareOfSums(self, aRange):
        return (sum(aRange))**2
        
    def determineOccurrence(self, aNumber):
        conn = neo4j.connect('http://localhost:7474')
        try: 
            curs = conn.cursor()
            curs.execute(MATCH_FORMAT % aNumber)
            if (curs.rowcount): # we have seen this differential before
                diff = curs.fetchone()
                updCnt = diff[0]['count']+ 1
                curs = conn.cursor()
                curs.execute(UPDATE_FORMAT % (aNumber, updCnt))
                conn.commit()
                return updCnt
            else: # no previous differential of this number
                curs = conn.cursor()
                curs.execute(CREATE_FORMAT % aNumber)
                conn.commit()
                return 1
        finally:
            conn.close()
            


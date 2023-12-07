from django.db import models
from django.utils.html import escape

"""
Rollback Concept:
My name is Aprit

deltas = [
    {
        ops: [
            { insert: 'My'},
            { insert: ' name' },
            { insert: ' is'},
            { insert: ' Ankur'},
        ]
    },
    {
        ops: [
            { delete: 'Ankur'},
            { insert: 'Arpit' },
        ]
    },
]
"""
class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    compressed_content = models.BinaryField(blank=True)
    is_draft = models.BooleanField(default=True)

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
        ('NEED_CORRECTION', 'Need Correction'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    # def rollback_changes(self):
    #     if self.deltas:
    #         last_delta = self.deltas.pop()
    #         # Apply the reverse of the last delta to rollback changes
    #         reversed_delta = {'ops': []}
    #         for op in reversed(last_delta['ops']):
    #             if 'insert' in op:
    #                 reversed_delta['ops'].append({'delete': op['insert']})
    #             elif 'delete' in op:
    #                 reversed_delta['ops'].append({'insert': op['delete']})
    #             else:
    #                 reversed_delta['ops'].append(op)

    #         self.apply_delta(reversed_delta)
    #         self.save()

    #         return True
    #     else:
    #         return False
        
    # def apply_delta(self, delta):
    #     for op in delta.get('ops', []):
    #         if 'insert' in op:
    #             self.content = self.content[:op.get('retain', 0)] + op['insert'] + self.content[op.get('retain', 0):]
    #         elif 'delete' in op:
    #             start_index = op.get('retain', 0)
    #             end_index = start_index + op['delete']
    #             self.content = self.content[:start_index] + self.content[end_index:]
                
    #     # Escape all HTML and XSS attacks
    #     self.content = escape(self.content)
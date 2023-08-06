#include "int_iet.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* set the thing below to disable safety checks */
/* #define INT_IET_CHECK(t) if(int_iet_check(t)) {fprintf(stderr, "check failed\n"); exit(EXIT_FAILURE);} */
#define INT_IET_CHECK(t)

uint64_t uint64_rand()
{
    return ((uint64_t) rand()) | (((uint64_t) rand()) << 16) | (((uint64_t) rand()) << 32) | (((uint64_t) rand()) << 48);
}

void int_iet_init(int_iet_t t, unsigned int n)
{
    t->nb_labels = n;
    t->labels = (label *) malloc(n * sizeof(label));
    t->intervals = (interval *) malloc(2 * n * sizeof(interval));

    if((t->labels == NULL) || (t->intervals == NULL))
    {
        free(t->labels);
        free(t->intervals);
        fprintf(stderr, "ERROR (new_int_iet): allocation error\n");
        exit(EXIT_FAILURE);
    }
}

void int_iet_clear(int_iet_t t)
{
    free(t->labels);
    free(t->intervals);
}

void int_iet_set_labels_and_twin(int_iet_t t, int * labels, int * twin, int k)
{
    int i;
    int n = t->nb_labels;

    t->nb_labels = n;

    if(k <= 0 || k > 2*n)
    {
        fprintf(stderr, "ERROR (set_labels_and_twin): k should be at most 2n\n");
        exit(EXIT_FAILURE);
    }
    for(i = 0; i < 2*n; ++i)
    {
        if(labels[i] != labels[twin[i]])
        {
            fprintf(stderr, "ERROR (set_labels_and_twin): interval %d and its twin %d have different labels\n", i, twin[i]);
            exit(EXIT_FAILURE);
        }
        if(twin[twin[i]] != i)
        {
            fprintf(stderr, "ERROR (set_labels_and_twin): twin is not an involution %d->%d->%d\n",i,twin[i],twin[twin[i]]);
            exit(EXIT_FAILURE);
        }
    }

    t->top = t->intervals;
    t->bot = t->intervals + k;
    for(i = 0; i < 2*n; ++i)
    {
        (t->intervals)[i].lab = t->labels + labels[i];
        (t->intervals)[i].twin = t->intervals + twin[i];
    }
    for(i = 0; i < 2*n-1; ++i)
    {
        (t->intervals)[i].next = t->intervals + i+1;
        (t->intervals)[i+1].prev = t->intervals + i;
    }
    (t->intervals)[0].prev = NULL;
    (t->intervals)[k].prev = NULL;
    (t->intervals)[k-1].next = NULL;
    (t->intervals)[2*n-1].next = NULL;

    /* set the same_interval field using the twin array */
    for(i=0; i<k; ++i)
        (t->intervals)[i].lab->same_interval = (twin[i] < k);
    for(i=k; i<2*n; ++i)
        (t->intervals)[i].lab->same_interval = (twin[i] >= k);
}

void int_iet_set_lengths(int_iet_t t, uint64_t * lengths)
{
    unsigned int i;
    for(i = 0; i < t->nb_labels; ++i)
    {
        (t->labels)[i].length = lengths[i];
        (t->labels)[i].height = 1;
    }
}

/* for all pairs i, j of twins on the same interval: pick random number */
/* for all pairs of i on the two sides: pick random number */
void int_iet_set_random_lengths(int_iet_t t, uint64_t L)
{
    unsigned int k;
    uint64_t l;
    interval * i, *j;

    /* reset */
    for (k = 0; k < t->nb_labels; ++k)
    {
        (t->labels)[k].length = 0;
        (t->labels)[k].height = 1;
    }

    for(i = t->top; i != NULL; i = i->next)
    {
        if (i->lab->same_interval)
        {
            for (j = t->bot; j != NULL; j = j->next)
            {
                if (j->lab->same_interval)
                {
                    l = uint64_rand() % (L / ((t->nb_labels) * (t->nb_labels)));
                    if (!l) l = 1;
                    i->lab->length += l;
                    j->lab->length += l;
                }
            }
        }
        else
        {
            l = uint64_rand() % (L / (t->nb_labels));
            if (!l) l = 1;
            i->lab->length += l;
        }
    }
    for (j = t->bot; j != NULL; j = j->next)
    {
        if (!(j->lab->same_interval))
        {
            j->lab->length += uint64_rand() % (L / (t->nb_labels));
        }
    }
}

int int_iet_check(const int_iet_t t)
{
    interval * i;
    unsigned int j;
    int * seen;
    uint64_t ltop, lbot;

    if(t->nb_labels == 0)
    {
        if((t->top != NULL) || (t->bot != NULL))
        {
            fprintf(stderr, "check problem: if zero interval t->top and t->bot must be NULL\n");
            return 1;
        }
        return 0;
    }
    if((t->top == NULL) || (t->bot == NULL))
    {
        fprintf(stderr, "check problem: got nb_labels = %d but t->top or t->bot is NULL\n", t->nb_labels);
        return 1;
    }

    if(t->top->prev != NULL)
    {
        fprintf(stderr, "check problem: the first interval on top has somebody on its left!!\n");
        return 1;
    }
    if(t->bot->prev != NULL)
    {
        fprintf(stderr, "check problem: the first interval on bot has somebody on its left!\n");
        return 1;
    }

    // count the number of intervals on top and bot
    seen = (int *) malloc((t->nb_labels) * sizeof(int));
    if(seen == NULL)
    {
        fprintf(stderr, "check problem: allocation error\n");
        return 1;
    }
    memset(seen, 0, (t->nb_labels) * sizeof(int));

    for(i=t->top; i!=NULL; i=i->next) seen[(int) (i->lab - t->labels)] += 1;
    for(i=t->bot; i!=NULL; i=i->next) seen[(int) (i->lab - t->labels)] += 1;

    for(j=0; j<t->nb_labels; ++j)
    {
        switch(seen[j])
        {
            case 0:
            if((t->labels)[j].length != 0)
            {
                fprintf(stderr,"check problem: interval %d does not appear but has positive length\n", j);
                free(seen);
                return 1;
            }
            if((t->labels)[j].same_interval != 1)
            {
                fprintf(stderr,"check problem: interval %d does not appear but has same_interval != 1\n", j);
                free(seen);
                return 1;
            }
            break;

            case 1:
            fprintf(stderr,"check problem: interval %d appears only once\n",j);
            free(seen);
            return 1;
            break;

            case 2:
            if((t->labels)[j].length == 0)
            {
                fprintf(stderr, "check problem: interval %d does appear but has zero length\n", j);
                free(seen);
                return 1;
            }
            break;

            default:
            fprintf(stderr,"check problem: interval %d seen %d time on top\n", j, seen[j]);
            free(seen);
            return 1;
        }
    }
    free(seen);

    // check consistency of pointers and lengths
    ltop = 0;
    for(i=t->top; i!=NULL; i=i->next)
    {
        j = (unsigned int) (i->lab - t->labels);  // integer label of the subinterval

        ltop += i->lab->length;

        if((i->next != NULL) && (i->next->prev != i))
        {
            fprintf(stderr, "check problem: pointer error on top at label %lu\n", i->lab - t->labels);
            return 1;
        }
        if(i->twin->twin != i)
        {
            fprintf(stderr,"check problem: twin problem on top i=%lu i->twin=%lu i->twin->twin=%lu\n",
                        i - t->intervals,
                        i->twin - t->intervals,
                        i->twin->twin - t->intervals);
            return 1;
        }
        if(i->lab != i->twin->lab)
        {
            fprintf(stderr,"check problem: label problem on top\n");
            return 1;
        }
    }
    lbot = 0;
    for(i=t->bot; i!=NULL; i=i->next)
    {
        j = (unsigned int) (i->lab - t->labels);  // integer label of the subinterval

        lbot += i->lab->length;

        if((i->next != NULL) && (i->next->prev != i))
        {
            fprintf(stderr,"pointer error on bot\n");
            return 1;
        }
        if(i->twin->twin != i)
        {
            fprintf(stderr,"twin problem on bot\n");
            return 1;
        }
        if(i->lab != i->twin->lab)
        {
            fprintf(stderr,"label problem on bot");
            return 1;
        }
    }

    if(lbot != ltop)
    {
        fprintf(stderr, "length top=%lu while length bot=%lu\n", ltop, lbot);
        return 1;
    }

    return 0;
}


void iet_print(int_iet_t t)
{
    int_iet_fprint(stdout, t);
}

void int_iet_fprint(FILE * stream, int_iet_t t)
{
    interval * i;
    unsigned int j;

    // intervals
    for(i=t->top; i!=NULL; i=i->next)
        fprintf(stream, "%lu ", i->lab - t->labels);
    fprintf(stream, "\n");
    for(i=t->bot; i!=NULL; i=i->next)
        fprintf(stream, "%lu ", i->lab - t->labels);
    fprintf(stream, "\n");
    // lengths
    fprintf(stream, "lengths: ");
    for (j = 0; j < t->nb_labels; j++)
        fprintf(stream, "%lu ", (t->labels[j]).length);
    fprintf(stream, "\n");
    // heights
    fprintf(stream, "heights: ");
    for (j = 0; j < t->nb_labels; j++)
        fprintf(stream, "%lu ", (t->labels[j]).height);
    fprintf(stream, "\n");
}



int int_iet_num_cylinders(uint64_t * widths, uint64_t * heights, int_iet_t t)
/* widths: NULL or write only vector of cylinder widths                 */
/* heights: NULL or write only vector of cylinder heights               */
/* t: integral interval exchange                                        */
/* Warning: t is modified (but not the allocated memory)                */
{
    int nb_cyl = 0;
    uint64_t ltop;
    uint64_t lbot;
    uint64_t m,l;
    interval *i1, *i2, *itmp;
    int nonzero_labels = t->nb_labels;

    if (nonzero_labels == 0)
        return 0;

    ltop = t->top->lab->length;
    lbot = t->bot->lab->length;

    if(ltop < lbot)
    {
        i1 = t->top; t->top = t->bot; t->bot = i1;
        ltop = t->top->lab->length;
        lbot = t->bot->lab->length;
    }

    while(nonzero_labels)
    // at the beginning of each loop ltop >= lbot
    {
#ifdef VERBOSE
        printf("start new loop...\n");
#endif

        INT_IET_CHECK(t)

        if((ltop != t->top->lab->length) ||
           (lbot != t->bot->lab->length) ||
           (ltop == 0) ||
           (lbot == 0) ||
           (ltop < lbot))
        {
            fprintf(stderr, "ERROR (num_cylinders): invalid state at beginning of loop\n");
            int_iet_fprint(stderr, t);
            return -1;
        }
#ifdef VERBOSE
        printf("check ok\n");
#endif

#ifdef VERBOSE
        int_iet_print(t);
#endif
        if(ltop == lbot)
        { 
            if(t->top->lab == t->bot->lab)
            {
                // find a cylinder
#ifdef VERBOSE
                printf("-> find a cylinder in %d\n", (int) (t->top->lab - t->labels));
#endif

                if (widths != NULL)
                    widths[nb_cyl] = t->top->lab->length;
                if (heights != NULL)
                    heights[nb_cyl] = t->top->lab->height;
                nb_cyl += 1;

                // in order to simplify the check test we set same_interval to 1
                // and set the length to 0
                t->top->lab->same_interval = 1;
                t->top->lab->length = 0;

                t->top = t->top->next;
                t->bot = t->bot->next;
                if(t->top != NULL) t->top->prev = NULL;
                if(t->bot != NULL) t->bot->prev = NULL;
                
            }
            else
            {
#ifdef VERBOSE
                printf("-> same length but different intervals\n");
                printf("   remove interval %d\n", (int) (t->bot->lab - t->labels));
#endif
                // the label i2 is removed
                // we update the height and move the current i1 at the
                // position of i2->twin
                i1 = t->top;
                i2 = t->bot;

                i1->lab->height += i2->lab->height;

                if(i1->next->lab != i2->lab)
                {
                    // we need the if statement to ignore the case of
                    // ab ...
                    // b .. a ..
                    t->top = i1->next;
                    t->top->prev = NULL;
                    i2->twin->prev->next = i1;
                    i1->next = i2->twin->next;
                    i1->prev = i2->twin->prev;
                    if(i2->twin->next != NULL) i2->twin->next->prev = i1;
                }
                else
                {
                    i1->next = i1->next->next;
                    if(i1->next != NULL) i1->next->prev = i1;
                }
                t->bot = i2->next;
                t->bot->prev = NULL;

                // update the same_interval field
                i1->lab->same_interval ^= i2->lab->same_interval;
                i2->lab->same_interval  = 1;
                i2->lab->length         = 0;
                i2->lab->height         = 0;
            }
        
            nonzero_labels -= 1;

            if(nonzero_labels)
            {
                ltop = t->top->lab->length;
                lbot = t->bot->lab->length;
                if(ltop < lbot)
                {
                    i1 = t->top; t->top = t->bot; t->bot = i1;
                    l = ltop; ltop = lbot; lbot = l;
                }
            }
        }

        // here ltop > lbot and we perform rauzy induction
        else if(t->top->lab->same_interval)  // case when top/twin on the same side
        {
            // remove the bot invertval
#ifdef VERBOSE
            printf("-> different lengths ltop=%lu lbot=%lu and top twin on top (perform rauzy induction)\n",
                            ltop, lbot);
#endif
            // we set i1 to the last interval in the bottom that has to move
            i1 = t->bot;
            l = t->top->lab->length - i1->lab->length;
            i1->lab->height += t->top->lab->height;
            while(l > i1->next->lab->length)
            {
                i1 = i1->next;
                i1->lab->height += t->top->lab->height;
                l -= i1->lab->length;
            }

            // modify the set of intervals on the bottom:
            //   - we exchange next <-> prev
            //   - we switch same_interval
            i2 = i1;
            while(i2 != NULL)
            {
                itmp = i2->prev;
                i2->prev = i2->next;
                i2->next = itmp;
                i2->lab->same_interval ^= 1;
                i2 = itmp;
            }

            // make the junctions
            i2 = t->top->twin->next;
            t->top->twin->next = i1;
            if(i2 != NULL)
                i2->prev = t->bot;
            t->bot->next = i2;
            t->bot = i1->prev;
            i1->prev->prev = NULL;
            i1->prev = t->top->twin;

            // set t->top to its new length
            t->top->lab->length = l;

            // switch top/bot for next loop
            i1 = t->top; t->top = t->bot; t->bot = i1;
            ltop = t->top->lab->length;
            lbot = t->bot->lab->length;
#ifdef VERBOSE
            printf("rauzy induction done\n");
            int_iet_check(t);
            printf("check ok\n");
            int_iet_print(t);
            fflush(stdout);
#endif
        }

        else // rauzy induction with top twin in the bottom
        {
            // rauzy induction
#ifdef VERBOSE
            printf("-> different lengths ltop=%lu lbot=%lu and top twin on bot (perform rauzy induction)\n",
                            ltop, lbot);
#endif
            // the multiplicative step
            l = 0;
            for(i1 = t->top->twin->prev; i1 != NULL; i1 = i1->prev)
                l += i1->lab->length;
            m = (unsigned int) (ltop / l);
            ltop -= m * l;
            if(ltop == 0)
            {
                // this is similar to the case where we remove an interval. We
                // need to translate a whole chunk of subintervals on the bottom
                // instead, we set the big length to the sum of the small lengths
                ltop = l;
                m -= 1;
            }

            for (i1 = t->top->twin->prev; i1 != NULL; i1 = i1->prev)
                i1->lab->height += m * t->top->lab->height;

            t->top->lab->length = ltop;
#ifdef VERBOSE
            printf("after multiplicative step top length is %lu\n", ltop);
#endif

            // the additive step (at each step we insert the first interval in the
            // bottom on the left of the twin top)
            while(ltop > lbot)
            {
#ifdef VERBOSE
                printf(" additive step bot=%d\n", (int) (t->bot->lab - t->labels));
                fflush(stdout);
#endif
                ltop -= lbot;
                t->top->lab->length = ltop;
                t->bot->lab->height += t->top->lab->height;

                i1 = t->bot; // the interval which moves
                i2 = t->top->twin; // the interval to which i1 moves to the left
                if (i1 != i2->prev)
                {
                    // remove i1 from the bottom
                    t->bot = i1->next;
                    t->bot->prev = NULL;

                    // place i1 before i2
                    i1->prev = i2->prev;
                    i1->next = i2;
                    i2->prev->next = i1;
                    i2->prev = i1;
                    lbot = t->bot->lab->length;
                }
#ifdef VERBOSE
                printf(" additive step done\n");
                int_iet_check(t);
                printf("check ok\n");
                int_iet_print(t);
                fflush(stdout);
#endif
            }
            i1 = t->top; t->top = t->bot; t->bot = i1;
            ltop = t->top->lab->length;
            lbot = t->bot->lab->length;

        }
    // end of the while loop
    }

    return nb_cyl;
}

